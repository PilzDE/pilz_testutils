from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository

ENABLE_TEXT = "* [ ] Perform hardware tests"
ALLOW_TEXT = "Allow hw-tests up to commit "


class GitHubPullRequestAnalyzer(object):
    def __init__(self, repo, token, allowed_users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        g = Github(token)
        self._repo: Repository = g.get_repo(repo)
        self._current_pr: PullRequest = None
        self._allowed_users = allowed_users

    def get_testable_pull_requests(self):
        testable_pull_requests = []
        print("%s\nSearching for PRs to test.\n" % (">"*50))
        for pr in self._repo.get_pulls():
            self._current_pr = pr
            if self._validate_pr():
                print("PR: #%s is enabled and ready for testing" % pr.number)
                testable_pull_requests.append(pr)
        print("<"*50)
        return testable_pull_requests

    def _validate_pr(self):
        return self._current_pr.state == "open" \
            and self._description_contain_enable_string() \
            and self._pr_is_allowed() \
            and self._not_tested_yet()

    def _not_tested_yet(self):
        last_commit = list(self._current_pr.get_commits())[-1]
        for c in self._current_pr.get_issue_comments():
            if c.user.login in self._allowed_users \
               and c.body.startswith("Finished test of %s" % last_commit.sha[:7]):
                print("PR: #%s is already tested" % self._current_pr.number)
                return False
        return True

    def _pr_is_internal(self):
        return self._current_pr.base.repo.full_name == self._current_pr.head.repo.full_name

    def _pr_is_allowed(self):
        return self._pr_is_internal() or self._head_commit_is_allowed_by_comment()

    def _head_commit_is_allowed_by_comment(self):
        for c in self._current_pr.get_issue_comments():
            if c.user.login in self._allowed_users and c.body.find(ALLOW_TEXT + self._current_pr.head.sha) != -1:
                return True

    def _description_contain_enable_string(self):
        if self._current_pr.body.find(ENABLE_TEXT) != -1:
            return True
        print("PR: #%s requests no hardware-test" % self._current_pr.number)
        return False
