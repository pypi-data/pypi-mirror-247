﻿"""_2300.py

RingPinsToDiscConnection
"""


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import _2240
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsToDiscConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnection',)


class RingPinsToDiscConnection(_2240.InterMountableComponentConnection):
    """RingPinsToDiscConnection

    This is a mastapy class.
    """

    TYPE = _RING_PINS_TO_DISC_CONNECTION

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_stiffness(self) -> 'float':
        """float: 'ContactStiffness' is the original name of this property."""

        temp = self.wrapped.ContactStiffness

        if temp is None:
            return 0.0

        return temp

    @contact_stiffness.setter
    def contact_stiffness(self, value: 'float'):
        self.wrapped.ContactStiffness = float(value) if value is not None else 0.0
