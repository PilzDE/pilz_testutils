#!/bin/bash -x

log_ws_info()
{
  echo "ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH"
}


test_for_correct_publish()
{
  test_name="acceptancetest_publish_test"
  rostest $REPO_NAME hwtest_scan_compare.test --results-base-dir "$LOG_FOLDER_NAME"
}

log_ws_info
test_for_correct_publish