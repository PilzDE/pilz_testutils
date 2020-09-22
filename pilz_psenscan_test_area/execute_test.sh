#!/bin/bash

source_ws()
{
  source "$CATKIN_WS_DIR/devel/setup.bash" 2>&1
}

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
  rosrun $REPO_NAME acceptancetest_publish_test 2>&1 && kill $PID 2>&1 && echo "Test successful" && wait && exit 0
  kill $PID 2>&1 && { echo "Test failed"; wait; exit 1; }
}

source_ws
log_ws_info
launch_psen_scan_node
test_for_correct_publish