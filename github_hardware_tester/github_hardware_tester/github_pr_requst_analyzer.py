from github import Github
import time
import datetime

ENABLE_TEXT = "* [ ] Perform hardware tests"
ALLOW_TEXT = "Allow hw-tests for "

# pr.create_issue_comment("Thank you!")


class GitHubPullRequestAnalyzer(object):
    def __init__(self, namespace, repo, token, allowed_users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        g = Github(token)
        self._repo = g.get_repo("%s/%s" % (namespace, repo))
        self._current_pr = None
        self._allowed_users = allowed_users

    def get_testable_pull_requests(self):
        testable_pull_requests = []
        print("="*30)
        for pr in self._repo.get_pulls():
            self._current_pr = pr
            if self._validate_pr():
                print("PR: #", pr.number, " is enabled and ready for testing")
                testable_pull_requests.append(pr)
        return testable_pull_requests

    def _validate_pr(self):
        return self._current_pr.state == "open" \
            and self._tests_enabled() \
            and self._critical_commits_permitted() \
            and self._not_tested_yet()

    def _get_datetime_from_str(self, last_change_str) -> datetime.datetime:
        return datetime.datetime.strptime(last_change_str, "%a, %d %b %Y %H:%M:%S GMT")

    def _not_tested_yet(self):
        last_commit = list(self._current_pr.get_commits())[-1]
        for c in self._current_pr.get_issue_comments():
            if c.user.login in self._allowed_users \
               and c.body.startswith("Finished test of %s" % last_commit.sha[:7]):
                print("PR: #%s is already tested" % self._current_pr.number)
                return False
        return True

    def _critical_commits_permitted(self):
        critical_commits = []
        for c in self._current_pr.get_commits():
            if c.author.login not in self._allowed_users:
                critical_commits.append(c)
        self._delete_permitted_commits(critical_commits)
        if len(critical_commits) > 0:
            print("PR: #%s has %s critical commits without permission" %
                  (self._current_pr.number, len(critical_commits)))
        return len(critical_commits) == 0

    def _tests_enabled(self):
        if self._current_pr.body.find(ENABLE_TEXT) != -1:
            return True
        print("PR: #%s requests no hardware-test" % self._current_pr.number)
        return False

    def _read_comments(self):
        pr_comments = []
        for c in self._current_pr.get_issue_comments():
            pr_comments.append(c)
        for r in self._current_pr.get_reviews():
            pr_comments.append(r)
        for c in self._current_pr.get_review_comments():
            pr_comments.append(c)
        return pr_comments

    def _delete_permitted_commits(self, critical_commits):
        for c in self._read_comments():
            for cc in critical_commits.copy():
                if c.user.login in self._allowed_users \
                   and c.body.find(ALLOW_TEXT + cc.sha[:7]) != -1:
                    critical_commits.remove(cc)
