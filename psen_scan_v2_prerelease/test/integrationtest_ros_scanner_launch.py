#!/usr/bin/env python

import unittest
import rosnode
import rospy

class TestStartup(unittest.TestCase):
    def test_startup(self):
        i = 0
        expectedNode = '/laser_scanner'
        while not expectedNode in rosnode.get_node_names():
            rospy.sleep(rospy.Duration(0.5))
            self.assertLess(i, 10, msg="node did not come up in the expected time") # wait 5s max
            i += 1

if __name__ == '__main__':
    import rostest
    rospy.init_node('test_ros_scanner_launch')
    rostest.rosrun('psen_scan_v2_prerelease', 'test_startup', TestStartup)
