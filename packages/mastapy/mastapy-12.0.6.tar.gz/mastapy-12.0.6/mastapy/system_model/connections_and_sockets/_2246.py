﻿"""_2246.py

PlanetaryConnection
"""


from mastapy.system_model.connections_and_sockets import _2254
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnection',)


class PlanetaryConnection(_2254.ShaftToMountableComponentConnection):
    """PlanetaryConnection

    This is a mastapy class.
    """

    TYPE = _PLANETARY_CONNECTION

    def __init__(self, instance_to_wrap: 'PlanetaryConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
