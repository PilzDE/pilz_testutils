# Copyright (c) 2019 Pilz GmbH & Co. KG
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

"""API for easy usage of Pilz robot test facility."""

import time
import threading

from op_modes import OperationMode
from test_facility_api import TestFacilityControlAPI
from test_facility_modbus_client import TestFacilityModbusClient


class TestFacilityManager(TestFacilityControlAPI):

    def __init__(self, client=TestFacilityModbusClient()):
        self._client = client
        # Lock to ensure that push and release operation of acknowledge button can be performed atomically
        self._push_and_release_lock = threading.RLock()

    def __enter__(self):
        self._client.open()

    def __exit__(self, type_in, value, tb):
        self.shutdown_robot()
        self._client.close()

    def choose_operation_mode(self, op_mode):
        """See base class."""

        self._client.set_T1_IO_to(False)
        self._client.set_T2_IO_to(False)
        self._client.set_Auto_IO_to(False)

        if op_mode == OperationMode.T1:
            self._client.set_T1_IO_to(True)
        elif op_mode == OperationMode.T2:
            self._client.set_T2_IO_to(True)
        elif op_mode == OperationMode.Auto:
            self._client.set_Auto_IO_to(True)

    def activate_emergency(self):
        """See base class."""
        self._client.set_Emergency_IO_to(False)

    def disable_emergency(self):
        """See base class."""
        self._client.set_Emergency_IO_to(True)
        # The disabling takes a while
        time.sleep(0.5)

    def acknowledge_ready_signal(self):
        """See base class."""
        with self._push_and_release_lock:
            self._client.set_Acknowledge_IO_to(True)
            # To realistically simulate the user action "push" and "release", we wait here for a while
            time.sleep(1.0)
            self._client.set_Acknowledge_IO_to(False)

    def activate_enabling(self):
        """See base class."""
        self._client.set_Enabling_IO_to(True)
        # Wait till enabling is given by FS controller
        time.sleep(0.5)

    def deactivate_enabling(self):
        """See base class."""
        self._client.set_Enabling_IO_to(False)

    def ready_robot_for_motion_in(self, op_mode):
        self.choose_operation_mode(op_mode)
        self.acknowledge_ready_signal()

        self.disable_emergency()
        self.acknowledge_ready_signal()

        if op_mode != OperationMode.Auto:
            self.activate_enabling()

    def shutdown_robot(self):
        self.deactivate_enabling()

        self.activate_emergency()

        self.choose_operation_mode(OperationMode.T1)
        self.acknowledge_ready_signal()
