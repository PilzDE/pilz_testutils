cmake_minimum_required(VERSION 2.8.3)
project(pilz_test_facility)

find_package(catkin REQUIRED COMPONENTS
  roslint
  rospy
)

#############
## Install ##
#############

catkin_python_setup()
