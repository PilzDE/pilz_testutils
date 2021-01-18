#!/bin/bash

[[ -z $TEST_AREA_SCRIPTS_PATH ]] && { echo "Environment variable TEST_AREA_SCRIPTS_PATH is not set! Cannot continue!" >&2; exit 1; }
[[ -z $1 ]] && export TARGET_BRANCH="melodic-devel" || export TARGET_BRANCH="$1"
[[ -z $2 ]] || export TEST_DURATION="$2"
[[ -z $3 ]] && export STANDALONE="false" || export STANDALONE="$3"


TMP_DIR="/tmp"
CATKIN_WS_NAME="catkin_ws"
export CATKIN_WS_DIR="$TMP_DIR/$CATKIN_WS_NAME"
export SRC_DIR="$CATKIN_WS_DIR/src"
export REPO_NAME="psen_scan_v2"
export REPO_DIR="$SRC_DIR/$REPO_NAME"
export LOG_DIR="/var/log/automatic_acceptance_test"
export LOG_FOLDER_NAME=$LOG_DIR"/$(date '+%Y_%m_%d_%H_%M_%S')_"$REPO_NAME


exit_failure()
{
  echo -e "\033[1;31mError! $1" >&2
  echo -e "\033[1;31mTest failed!" >&2
  echo -e "\033[1;37mTo run the test again, please execute '$TEST_AREA_SCRIPTS_PATH/automatic_acceptance_test_psen_scan.sh'"
  exit 1
}

create_log_file()
{
  mkdir -p "$LOG_FOLDER_NAME"
  LOG_FILE_NAME="$(date '+%Y_%m_%d_%H_%M_%S')_"$REPO_NAME"_automatic_acceptance_test_log.txt"
  LOG_FILE="$LOG_FOLDER_NAME/$LOG_FILE_NAME"
  touch $LOG_FILE 2> /dev/null || { LOG_DIR="/home/$USER"; LOG_FILE="$LOG_DIR/$LOG_FILE_NAME"; echo "Cannot create system logfile." >&2; }
  touch $LOG_FILE 2> /dev/null || exit_failure "Cannot create local logfile."
  echo "Logging to $LOG_FILE."
}

source_ROS()
{
  source /opt/ros/melodic/setup.bash 2>> $LOG_FILE || exit_failure "Sourcing ROS failed!"
}

source_ws()
{
  source "$CATKIN_WS_DIR/devel/setup.bash"
}

print_separator()
{
  separator=""
  for i in $(seq 20)
  do
    separator+=$1
  done
  echo $separator
}

log_file_section()
{
  print_separator $2 >> $LOG_FILE
  echo $1 >> $LOG_FILE
  print_separator $2 >> $LOG_FILE
}

start_log_file_section()
{
  log_file_section "$1" ">"
}

end_log_file_section()
{
  log_file_section "$1" "<"
}

execute_section()
{
  # Parse section name from script name by:
  # 1. Taking away the preceding path and .sh suffix
  # 2. Replacing underscores with spaces
  section_name=$(echo "$1" | sed -E 's/.*\/([a-zA-Z_]+)\.sh/\1/;s/_/ /g')
  echo -e "\033[0;36m$section_name ...\033[0m"
  start_log_file_section "$section_name"
  stdbuf -o 0 $@ | tee -a $LOG_FILE
  [[ ${PIPESTATUS[0]} != 0 ]] && exit_failure "$1 failed!"
  end_log_file_section "$section_name"
  echo -e "\033[0;36m$section_name done\033[0m"
}

create_log_file
source_ROS

execute_section "$TEST_AREA_SCRIPTS_PATH/update_system_packages.sh"

execute_section "$TEST_AREA_SCRIPTS_PATH/setup_workspace.sh"
source_ws
execute_section "$TEST_AREA_SCRIPTS_PATH/execute_test.sh"

echo -e "\033[0;32mTest successful\033[0m"
exit 0
