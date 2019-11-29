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

from tfc_api import TestFacilityControlAPI
from op_modes import OperationMode

# The register used to tell the FS-controller to active the emergency.
_EMERGENCY_REGISTER = 0
_ENABLING_REGISTER = 1
_OPERATION_MODE_T1_REGISTER = 2
_OPERATION_MODE_T2_REGISTER = 3
_OPERATION_MODE_AUTO_REGISTER = 4
_ACKNOWLEDGE_REGISTER = 5


class ModbusTfcAPI(TestFacilityControlAPI):

    def __init__(self, client):
        self._client = client
        # Lock to ensure that push and release operation of acknowledge button can be performed atomically
        self._push_and_release_lock = threading.RLock()

    def open(self):
        self._client.open()

    def close(self):
        self._client.close()
        self._client = None

    def choose_operation_mode(self, op_mode):
        """See base class."""
        if op_mode == OperationMode.T1:
            register = _OPERATION_MODE_T1_REGISTER
        elif op_mode == OperationMode.T2:
            register = _OPERATION_MODE_T2_REGISTER
        elif op_mode == OperationMode.Auto:
            register = _OPERATION_MODE_AUTO_REGISTER
        self._client.write(register, True)

    def activate_emergency(self):
        """See base class."""
        self._client.write(_EMERGENCY_REGISTER, False)

    def disable_emergency(self):
        """See base class."""
        self._client.write(_EMERGENCY_REGISTER, True)

    def acknowledge_ready_signal(self):
        """See base class."""
        with self._push_and_release_lock:
            self._client.write(_ACKNOWLEDGE_REGISTER, True)
            time.sleep(1.0)
            self._client.write(_ACKNOWLEDGE_REGISTER, False)

    def activate_enabling(self):
        """See base class."""
        self._client.write(_ENABLING_REGISTER, True)

    def deactivate_enabling(self):
        """See base class."""
        self._client.write(_ENABLING_REGISTER, False)

