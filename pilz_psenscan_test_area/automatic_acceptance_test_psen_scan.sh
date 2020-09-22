#!/bin/bash

[[ -z $1 ]] && export TARGET_BRANCH="melodic-devel" || export TARGET_BRANCH="$1"

TMP_DIR="/tmp"
CATKIN_WS_NAME="catkin_ws"
export CATKIN_WS_DIR="$TMP_DIR/$CATKIN_WS_NAME"
export SRC_DIR="$CATKIN_WS_DIR/src"
export REPO_NAME="psen_scan"
export REPO_DIR="$SRC_DIR/$REPO_NAME"

create_log_file()
{
  LOG_DIR="/var/log/automatic_acceptance_test"
  mkdir $LOG_DIR 2> /dev/null
  
  LOG_FILE_NAME="$(date '+%Y_%m_%d_%H_%M_%S')_"$REPO_NAME"_automatic_acceptance_test_log.txt"
  LOG_FILE="$LOG_DIR/$LOG_FILE_NAME"
  touch $LOG_FILE 2> /dev/null || { LOG_DIR="/home/$USER"; LOG_FILE="$LOG_DIR/$LOG_FILE_NAME"; echo "Cannot create system logfile." >&2; }
  touch $LOG_FILE 2> /dev/null || { echo "Cannot create local logfile." >&2; exit 1; }
  echo "Logging to $LOG_FILE."
}

source_ROS()
{
  source /opt/ros/melodic/setup.bash 2>> $LOG_FILE || { echo "Error!" >&2; exit 1; }
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
  section_name=$(echo "$1" | sed -E 's/.*\/([a-zA-Z_]+)\.sh/\1/;s/_/ /g')
  echo "$section_name ..."
  start_log_file_section "$section_name"
  $@ >> $LOG_FILE || { echo "Error!" >&2; exit 1; }
  end_log_file_section "$section_name"
  echo "done"
}

create_log_file
source_ROS

execute_section "$TEST_AREA_SCRIPTS_PATH/update_system_packages.sh"

execute_section "$TEST_AREA_SCRIPTS_PATH/setup_workspace.sh"

execute_section "$TEST_AREA_SCRIPTS_PATH/execute_test.sh"

echo "Test successful"
exit 0
