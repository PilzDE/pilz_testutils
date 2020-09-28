#!/bin/bash -x

log_ws_info()
{
  echo "ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH"
}

launch_psen_scan_node()
{
  roslaunch $REPO_NAME psen_scan.launch sensor_ip:=192.168.0.10 host_ip:=192.168.0.20& 2>&1
  PID=$!
  echo "Started Process $PID"
}

test_for_correct_publish()
{
  test_name="acceptancetest_publish_test"
  rosrun $REPO_NAME $test_name 2>&1 && kill $PID 2>&1 && echo "$test_name successful" && wait && exit 0
  kill $PID 2>&1 && { echo "$test_name failed"; wait; exit 1; }
}

log_ws_info
launch_psen_scan_node
test_for_correct_publish