#!/bin/bash -x

create_catkin_ws()
{
  mkdir -p "$SRC_DIR" 2>&1
  catkin init --workspace "$CATKIN_WS_DIR"
}

clone_repo()
{
  ls "$REPO_DIR" > /dev/null 2>&1 && rm -rf "$REPO_DIR" 2>&1
  git clone --branch "$TARGET_BRANCH" "https://github.com/PilzDE/$REPO_NAME.git" "$REPO_DIR" 2>&1 || exit 1
}

log_repo_info()
{
  cd "$REPO_DIR"
  # Parse the currently checked out branch and commit hash
  branch=$(git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')
  commit_hash=$(git log -1 | sed -e '/^[^c]/d' -e 's/commit \(.*\)/\1/')
  echo "repo: $REPO_NAME"
  echo "branch: $branch"
  echo "commit: $commit_hash"
}

build_ws()
{
  catkin config --cmake-args -DENABLE_HARDWARE_TESTING=ON
  catkin config --workspace /tmp/catkin_ws
  catkin build
  catkin build --make-args tests
}

create_catkin_ws
clone_repo
log_repo_info
build_ws
