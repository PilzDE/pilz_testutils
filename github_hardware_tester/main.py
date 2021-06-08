"""Automated Hardware Testing

Usage:
   github_hardware_tester.py REPO ALLOWED_USERS ... [--log=LOG_DIR] [--docker_opts=DOCKER_OPTS] [--apt_proxy=APT_PROXY] [--cmake_args=CMAKE_ARGS]

   e.g. github_hardware_tester.py max/awesome_repo max theOtherOne AwesomeGuy

Options:
    -h --help                   show this
    --log=LOG_DIR               test log directory [default: ~/.ros/hardware_tests/]
    --docker_opts=DOCKER_OPTS   options that will be passed to the industrial ci
    --cmake_args=CMAKE_ARGS     arguments that will be passed to the cmake run
    --apt_proxy=APT_PROXY
"""


from github_hardware_tester import GitHubPullRequestAnalyzer, ask_user_for_pr_to_check, HardwareTester
import os
import sys
import docopt
import contextlib

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def _get_github_token():
    TOKEN = ""
    try:
        with open(os.path.join(os.path.dirname(__file__), 'TOKEN'), 'r') as f:
            TOKEN = f.readline()
    except FileNotFoundError:
        print("Please create a 'TOKEN' file with a valid github token to access the repository next to the main.py")
        return 0
    return TOKEN


def _define_args():
    pass


if __name__ == "__main__":
    # print(sys.argv[1:])
    arguments = docopt.docopt(__doc__)
    print(arguments)
    repo = arguments.get("REPO")
    log_dir = os.path.expanduser(arguments.get("--log"))
    docker_opts = arguments.get("--docker_opts")
    cmake_args = arguments.get("--cmake_args")
    allowed_users = arguments.get("ALLOWED_USERS")
    apt_proxy = arguments.get("--apt_proxy")

    token = _get_github_token()

    analyzer = GitHubPullRequestAnalyzer(
        repo, token, allowed_users)
    tester = HardwareTester(docker_opts=docker_opts,
                            cmake_args=cmake_args,
                            token=token,
                            apt_proxy=apt_proxy,
                            repo=repo,
                            log_dir=log_dir)

    with contextlib.suppress(KeyboardInterrupt):
        tester.check_prs(ask_user_for_pr_to_check(
            analyzer.get_testable_pull_requests()))
