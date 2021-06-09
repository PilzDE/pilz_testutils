#! /usr/bin/env python

"""Automated Hardware Testing

Usage:
    github_hardware_tester.py REPO ALLOWED_USERS ... --token=TOKEN
        [--log=LOG_DIR]
        [--docker_opts=DOCKER_OPTS]
        [--apt_proxy=APT_PROXY]
        [--cmake_args=CMAKE_ARGS]
        [--setup_cmd=SETUP_CMD]
        [--cleanup_cmd=SETUP_CMD]
        [--loop_time=MIN_TIME_IN_SEC]

   e.g. github_hardware_tester.py max/awesome_repo max theOtherOne AwesomeGuy

Options:
    -h --help                    Show this
    --log=LOG_DIR                Test log directory [default: ~/.ros/hardware_tests/]
    --token=TOKEN                GitHub personal access token with "public_repo" scope
    --docker_opts=DOCKER_OPTS    Options that will be passed to the industrial ci
    --cmake_args=CMAKE_ARGS      Arguments that will be passed to the cmake run
    --apt_proxy=APT_PROXY
    --setup_cmd=SETUP_CMD        Command to run before starting industrial_ci e.g. for starting hardware
    --cleanup_cmd=CLEANUP_CMD    Command to run after industrial_ci has finished e.g. for stopping hardware
    --loop_time=MIN_TIME_IN_SEC  If set automatically searches valid pull requests and executes the tests continuosly.
                                 The argument provided is the minimum repeat time of the loop in seconds.
"""


from github_hardware_tester import GitHubPullRequestAnalyzer, ask_user_for_pr_to_check, HardwareTester
import os
import sys
import time
import docopt
import contextlib

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def check_and_execute_loop(loop_time):
    while True:
        start = time.time()
        tester.check_prs(analyzer.get_testable_pull_requests())
        end = time.time()
        remain = int(loop_time) - (end - start)
        if remain > 0:
            time.sleep(remain)


if __name__ == "__main__":
    arguments = docopt.docopt(__doc__)
    print(arguments)
    repo = arguments.get("REPO")
    log_dir = os.path.expanduser(arguments.get("--log"))
    token = arguments.get("--token")
    docker_opts = arguments.get("--docker_opts")
    cmake_args = arguments.get("--cmake_args")
    allowed_users = arguments.get("ALLOWED_USERS")
    apt_proxy = arguments.get("--apt_proxy")
    setup_cmd = arguments.get("--setup_cmd")
    cleanup_cmd = arguments.get("--cleanup_cmd")
    loop_time = arguments.get("--loop_time", None)

    analyzer = GitHubPullRequestAnalyzer(
        repo, token, allowed_users)
    tester = HardwareTester(docker_opts=docker_opts,
                            cmake_args=cmake_args,
                            token=token,
                            apt_proxy=apt_proxy,
                            repo=repo,
                            log_dir=log_dir,
                            setup_cmd=setup_cmd,
                            cleanup_cmd=cleanup_cmd)

    with contextlib.suppress(KeyboardInterrupt):
        if not loop_time:
            tester.check_prs(ask_user_for_pr_to_check(
                analyzer.get_testable_pull_requests()))
        else:
            check_and_execute_loop(loop_time)
