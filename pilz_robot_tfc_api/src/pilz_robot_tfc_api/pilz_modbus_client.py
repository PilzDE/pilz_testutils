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

from modbus_client import ModbusClient


class NoOpenConnection(OSError):
    """Exception indicating that no connection to the Modbus server is open."""
    pass


class PilzModbusClient(ModbusClient):
    """Implementation of the abstract ModbusClient class using the pymodbus lib"""
    _client = None

    def _is_connection_open(self):
        """See base class."""
        if self._client is None:
            return False
        else:
            return True

    def open(self):
        """See base class."""
        if self._is_connection_open():
            return
        self._client = ModbusTcpClient('169.254.60.99', 502)
        self._client.connect()

    def close(self):
        """See base class."""
        if not self._is_connection_open():
            return
        self._client.close()
        self._client = None

    def read(self, start_register, end_register):
        """See base class."""
        if not self._is_connection_open():
            raise NoOpenConnection("No open connection to server")
        return self._client.read_coils(start_register, end_register)

    def write(self, register, value):
        """See base class."""
        if not self._is_connection_open():
            raise NoOpenConnection("No open connection to server")
        response = self._client.write_coil(register, value)


