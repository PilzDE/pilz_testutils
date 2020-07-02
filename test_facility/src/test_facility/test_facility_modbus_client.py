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

from pymodbus.client.sync import ModbusTcpClient

# The register used to tell the FS-controller to active the emergency.
_EMERGENCY_REGISTER = 0
_ENABLING_REGISTER = 1
_OPERATION_MODE_T1_REGISTER = 2
_OPERATION_MODE_T2_REGISTER = 3
_OPERATION_MODE_AUTO_REGISTER = 4
_ACKNOWLEDGE_REGISTER = 5


class NoOpenConnection(OSError):
    """Exception indicating that no connection to the Modbus server is open."""
    pass


class TestFacilityModbusClient(object):
    """Modbus client to communicate with robot test facility using the pymodbus lib"""
    _client = None

    def _is_connection_open(self):
        if self._client is None:
            return False
        else:
            return True

    def open(self):
        if self._is_connection_open():
            return
        self._client = ModbusTcpClient('169.254.60.99', 502)
        self._client.connect()

    def close(self):
        if not self._is_connection_open():
            return
        self._client.close()
        self._client = None

    def read(self, start_register, end_register):
        if not self._is_connection_open():
            raise NoOpenConnection("No open connection to server")
        return self._client.read_coils(start_register, end_register)

    def write(self, register, value):
        if not self._is_connection_open():
            raise NoOpenConnection("No open connection to server")
        response = self._client.write_coil(register, value)

    def set_T1_IO_to(self, flag):
        self.write(_OPERATION_MODE_T1_REGISTER, flag)

    def set_T2_IO_to(self, flag):
        self.write(_OPERATION_MODE_T2_REGISTER, flag)

    def set_Auto_IO_to(self, flag):
        self.write(_OPERATION_MODE_AUTO_REGISTER, flag)

    def set_Emergency_IO_to(self, flag):
        self.write(_EMERGENCY_REGISTER, flag)

    def set_Acknowledge_IO_to(self, flag):
        self.write(_ACKNOWLEDGE_REGISTER, flag)

    def set_Enabling_IO_to(self, flag):
        self.write(_ENABLING_REGISTER, flag)
