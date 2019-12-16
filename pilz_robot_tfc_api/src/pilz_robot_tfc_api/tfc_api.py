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

from abc import ABCMeta, abstractmethod
from enum import Enum


class OperationMode(Enum):
    """ Declaration of the operation modes. """
    T1 = 0
    T2 = 1
    Auto = 2


class TestFacilityControlAPI(object):
    """ Declaration of the Pilz robot test facility control API. """
    __metaclass__ = ABCMeta

    @abstractmethod
    def choose_operation_mode(self, op_mode):
        """ Allows to change the operation mode. """
        pass

    @abstractmethod
    def activate_emergency(self):
        """ Triggers the emergency stop which causes the safety controller to execute a stop 1.

            This function causes the safety controller to perform the same actions,
            as if the user pushes the emergency button on the real facility.
        """
        pass

    @abstractmethod
    def disable_emergency(self):
        """ Releases the emergency stop.

            This function causes the safety controller to perform the same actions,
            as if the user releases the emergency button on the real facility.
        """
        pass

    @abstractmethod
    def acknowledge_ready_signal(self):
        """ Acknowledges the ready signal of the safety controller.

            This function causes the safety controller to perform the same actions,
            as if the user pushes and releases the acknowledge button on the real facility.
        """
        pass

    @abstractmethod
    def activate_enabling(self):
        """ Enables the drives.

            This function causes the safety controller to perform the same actions,
            as if the user pushes the enabling button on the real facility.
        """
        pass

    @abstractmethod
    def deactivate_enabling(self):
        """ Disables the drives.

            This function causes the safety controller to perform the same actions,
            as if the user releases the enabling button on the real facility.
        """
        pass

