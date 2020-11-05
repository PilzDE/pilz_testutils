#!/bin/bash -x

log_ws_info()
{
  echo "ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH"
}


test_scan_compare()
{
  TEST_FILE="hwtest_scan_compare.test"
  TEST_ARGS="${TEST_DURATION+test_duration:=$TEST_DURATION} --text --results-base-dir $LOG_FOLDER_NAME"
  rostest $REPO_NAME $TEST_FILE $TEST_ARGS 2>&1 || exit 1
}

log_test_results()
{
  catkin_test_results $LOG_FOLDER_NAME || exit 1
}

log_ws_info
test_scan_compare
log_test_results