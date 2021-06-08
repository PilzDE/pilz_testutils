
from tempfile import TemporaryDirectory
from pathlib import Path
from .print_redirector import PrintRedirector
import os
import time
import subprocess


class HardwareTester(object):
    def __init__(self, token, repo, log_dir, cmake_args, docker_opts, apt_proxy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token = token
        self._repo = repo
        self._log_dir = log_dir
        self._docker_opts = docker_opts
        self._cmake_args = cmake_args
        self._apt_proxy = apt_proxy

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
                    "git clone https://%s@github.com/%s.git" % (self._token, self._repo), t)
                repo_dir = os.path.join(t, self._repo.split("/")[1])
                run_subprocess(
                    "git config advice.detachedHead false", repo_dir)
                run_subprocess(
                    "git fetch origin pull/%s/merge" % pr.number, repo_dir)
                run_subprocess(
                    "git checkout FETCH_HEAD", repo_dir)
                result, test_output = run_tests(
                    repo_dir, self._docker_opts, self._cmake_args, self._apt_proxy)
                print(test_output)
        end_text = "Finished test of %s: %s" % (
            last_commit.sha[:7], "SUCCESSFULL" if not result else "WITH %s FAILURES" % result)
        print(end_text)
        pr.create_issue_comment(end_text)


def run_subprocess(command, dir):
    print(subprocess.check_output(command.split(" "),
                                  cwd=dir, stderr=subprocess.STDOUT).decode())


def run_tests(dir, docker_opts, cmake_args, apt_proxy):
    env = os.environ.copy()
    env['ROS_DISTRO'] = 'noetic'
    env['ROS_REPO'] = 'main'
    if docker_opts:
        env['DOCKER_RUN_OPTS'] = docker_opts
    if apt_proxy:
        env['APT_PROXY'] = apt_proxy
    if cmake_args:
        env['CMAKE_ARGS'] = cmake_args

    # Needs sources ROS and path to industrial_ci
    command = 'rosrun industrial_ci run_ci'
    print('Running {}'.format(command))
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, env=env, cwd=os.path.expanduser(dir))
    stdout_data, stderr_data = p.communicate()
    # print(stdout_data.decode('utf-8'))
    # ▶ rosrun industrial_ci run_ci ROS_DISTRO=noetic ROS_REPO=main DOCKER_RUN_OPTS="-v /usr/local/share/ca-certificates:/usr/local/share/ca-certificates:ro" APT_PROXY="http://172.20.20.104:3142"
    return p.returncode, stdout_data.decode('utf-8')
