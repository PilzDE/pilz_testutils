# Copyright (c) 2020 Pilz GmbH & Co. KG
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import rospy
import numpy
from moveit_commander import RobotCommander, MoveItCommanderException


def _are_joint_values_equal(joint_values_a, joint_values_b, tolerance):
    """True if the specified joint values are equal, otherwise False."""
    return numpy.allclose(joint_values_a, joint_values_b, atol=tolerance)


class TestFacilitySensors(object):
    """Abstraction layer for easy usage of the PILZ test facility sensors."""

    _DEFAULT_WAIT_TIME_FOR_MOTION_DETECTION_SEC = 3.0
    _DEFAULT_WAIT_TIME_IS_ROBOT_MOVING_SEC = 1.0
    _DEFAULT_TOLERANCE_FOR_MOTION_DETECTION_RAD = 0.01
    _DEFAULT_SLEEP_INTERVAL_SEC = 0.01
    _DEFAULT_GROUP_NAME = "manipulator"

    def __init__(self, group_name=_DEFAULT_GROUP_NAME):
        self._robot_commander = RobotCommander()
        self._group_name = group_name

    def set_default_motion_detection_tolerance(self, motion_tolerance_rad):
        self._DEFAULT_TOLERANCE_FOR_MOTION_DETECTION_RAD = motion_tolerance_rad

    def _get_current_joint_states(self):
        """Returns the current joint state values of the robot.
        :raises RobotCurrentStateError if given planning group does not exist.
        """
        return self._robot_commander.get_group(self._group_name).get_current_joint_values()

    def is_robot_at_position(self, expected_joint_values,
                             tolerance=_DEFAULT_TOLERANCE_FOR_MOTION_DETECTION_RAD):
        """True if the robot stands at the specified position, otherwise False."""
        return _are_joint_values_equal(self._get_current_joint_states(), expected_joint_values, tolerance)

    def is_robot_moving(self, wait_time_out=_DEFAULT_WAIT_TIME_IS_ROBOT_MOVING_SEC):
        """True if the robot is moving, otherwise false."""
        return self.wait_for_robot_motion(wait_time_out=wait_time_out)

    def _wait_till(self, motion_expected, wait_time_out, move_tolerance, sleep_interval):
        """Waits till the robot has started moving or until the robot has stopped, depending on the given parameters.
        """
        old_joint_values = self._get_current_joint_states()
        rospy.loginfo("Start joint values: " + str(old_joint_values))

        start_time = rospy.get_time()
        rospy.loginfo("Start observing robot motion...")

        while not rospy.is_shutdown():
            rospy.sleep(sleep_interval)
            curr_joint_values = self._get_current_joint_states()

            motion_detected = not _are_joint_values_equal(curr_joint_values, old_joint_values, move_tolerance)
            if motion_expected and motion_detected:
                rospy.loginfo("Motion detected at pose: " + str(curr_joint_values))
                return True

            if not motion_expected and not motion_detected:
                rospy.loginfo("Robot stands still at pose: " + str(curr_joint_values))
                return True

            if rospy.get_time() - start_time > wait_time_out:
                rospy.loginfo("Timeout reached")
                return False

    def wait_for_robot_motion(self,
                              wait_time_out=_DEFAULT_WAIT_TIME_FOR_MOTION_DETECTION_SEC,
                              move_tolerance=_DEFAULT_TOLERANCE_FOR_MOTION_DETECTION_RAD,
                              sleep_interval=_DEFAULT_SLEEP_INTERVAL_SEC):
        """Waits until a robot motion is detected."""
        return self._wait_till(motion_expected=True,
                               wait_time_out=wait_time_out,
                               move_tolerance=move_tolerance,
                               sleep_interval=sleep_interval)

    def wait_till_robot_stopped(self,
                                wait_time_out=_DEFAULT_WAIT_TIME_FOR_MOTION_DETECTION_SEC,
                                move_tolerance=_DEFAULT_TOLERANCE_FOR_MOTION_DETECTION_RAD,
                                sleep_interval=_DEFAULT_SLEEP_INTERVAL_SEC):
        """Waits till the robot stops it's motion."""
        return self._wait_till(motion_expected=False,
                               wait_time_out=wait_time_out,
                               move_tolerance=move_tolerance,
                               sleep_interval=sleep_interval)
