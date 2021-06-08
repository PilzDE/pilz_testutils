
from tempfile import TemporaryDirectory
from pathlib import Path
from .print_redirector import PrintRedirector
import os
import time
import subprocess


class HardwareTester(object):
    def __init__(self, token, repo, log_dir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token = token
        self._repo = repo
        self._log_dir = log_dir

    def check_prs(self, prs_to_check):
        for pr in prs_to_check:
            self.check_pr(pr)

    def _get_log_file_name(self, pr) -> str:
        return "%s_%s" % (list(pr.get_commits())[-1].sha,
                          time.strftime("(%Y%b%d_%H:%M:%S)", time.localtime()))

    def check_pr(self, pr):
        last_commit = list(pr.get_commits())[-1]
        pr.create_issue_comment("Starting a test for %s" % last_commit.sha)
        with PrintRedirector(Path(self._log_dir) / Path(self._get_log_file_name(pr))):
            with TemporaryDirectory() as t:
                run_subprocess(
                    "git clone https://%s@github.com/rfeistenauer/test_project.git" % self._token, t)
                repo_dir = os.path.join(t, self._repo)
                run_subprocess(
                    "git config advice.detachedHead false", repo_dir)
                run_subprocess(
                    "git fetch origin pull/%s/merge" % pr.number, repo_dir)
                run_subprocess(
                    "git checkout FETCH_HEAD", repo_dir)
                success, results = run_tests(repo_dir)
        end_text = "Finished test of %s: %s\n\n%s" % (
            last_commit.sha[:7], "SUCCESSFULL" if success else "WITH ERRORS", results)
        print(end_text)
        pr.create_issue_comment(end_text)


def run_subprocess(command, dir):
    print(subprocess.check_output(command.split(" "),
                                  cwd=dir, stderr=subprocess.STDOUT).decode())


def run_tests(dir):
    success = False
    results = "Error"
    # ▶ rosrun industrial_ci run_ci ROS_DISTRO=noetic ROS_REPO=main DOCKER_RUN_OPTS="-v /usr/local/share/ca-certificates:/usr/local/share/ca-certificates:ro" APT_PROXY="http://172.20.20.104:3142"
    return success, results
