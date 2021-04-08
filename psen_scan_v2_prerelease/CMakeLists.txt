cmake_minimum_required(VERSION 3.0.2)
project(psen_scan_v2_prerelease)

find_package(catkin REQUIRED)

###################################
## catkin specific configuration ##
###################################
catkin_package()

#############
## Testing ##
#############
if (CATKIN_ENABLE_TESTING)
  find_package(psen_scan_v2 REQUIRED)
  find_package(rosnode REQUIRED)
  find_package(rospy REQUIRED)
  find_package(rostest REQUIRED)

  add_rostest(test/integrationtest_ros_scanner_launch.test)
endif()
