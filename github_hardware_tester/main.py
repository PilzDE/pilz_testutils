
from github_hardware_tester import GitHubPullRequestAnalyzer, ask_user_for_pr_to_check, HardwareTester
import os
import sys
import contextlib

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def get_github_token():
    TOKEN = ""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'TOKEN'), 'r') as f:
            TOKEN = f.readline()
    except FileNotFoundError:
        print("Please create a 'TOKEN' file with a valid github token to access the repository next to the main.py")
        return 0
    return TOKEN


if __name__ == "__main__":
    NAME_SPACE = "rfeistenauer"
    REPO = "test_project"
    LOG_DIR = "/home/rfeistenauer/.ros/hardware_tests/"
    ALLOWED_USERS = ["rfeistenauer"]

    TOKEN = get_github_token()

    analyzer = GitHubPullRequestAnalyzer(
        NAME_SPACE, REPO, TOKEN, ALLOWED_USERS)
    tester = HardwareTester(TOKEN, REPO, LOG_DIR)

    with contextlib.suppress(KeyboardInterrupt):
        tester.check_prs(ask_user_for_pr_to_check(
            analyzer.get_testable_pull_requests()))
