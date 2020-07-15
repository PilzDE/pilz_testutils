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


class TestFacilityModbusClientMock(object):
    """This class allows to run the automated acceptance tests without a present test facility.

    To use this mock simply import:
    .. code-block:: python
        from pilz_test_facility.test_facility_modbus_client_mock import TestFacilityModbusClientMock

    and replace the original client with the mock, like this:
    .. code-block:: python
        test_facility_manager = TestFacilityManager()
        test_facility_manager._client = TestFacilityModbusClientMock()
    """

    def open(self):
        rospy.loginfo("ModbusClientMock: open() called")

    def close(self):
        rospy.loginfo("ModbusClientMock: close() called")

    def read(self, start_register, end_register):
        rospy.loginfo("ModbusClientMock: read(" + start_register + ", " + end_register + ") called")

    def write(self, register, value):
        rospy.loginfo("ModbusClientMock: write(" + register + ", " + value + ") called")

    def set_T1_IO_to(self, flag):
        rospy.loginfo("ModbusClientMock: set_T1_IO_to(" + str(flag) + ") called")

    def set_T2_IO_to(self, flag):
        rospy.loginfo("ModbusClientMock: set_T2_IO_to(" + str(flag) + ") called")

    def set_Auto_IO_to(self, flag):
        rospy.loginfo("ModbusClientMock: set_Auto_IO_to(" + str(flag) + ") called")

    def set_Emergency_IO_to(self, flag):
        rospy.loginfo("ModbusClientMock: set_Emergency_IO_to(" + str(flag) + ") called")

    def set_Acknowledge_IO_to(self, flag):
        rospy.loginfo("ModbusClientMock: set_Acknowledge_IO_to(" + str(flag) + ") called")

    def set_Enabling_IO_to(self, flag):
        rospy.loginfo("ModbusClientMock: set_Enabling_IO_to(" + str(flag) + ") called")