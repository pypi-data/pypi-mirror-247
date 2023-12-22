﻿"""_2298.py

CycloidalDiscPlanetaryBearingSocket
"""


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import _2248
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscPlanetaryBearingSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingSocket',)


class CycloidalDiscPlanetaryBearingSocket(_2248.PlanetarySocketBase):
    """CycloidalDiscPlanetaryBearingSocket

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_SOCKET

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_for_eccentric_bearing(self) -> 'bool':
        """bool: 'IsForEccentricBearing' is the original name of this property."""

        temp = self.wrapped.IsForEccentricBearing

        if temp is None:
            return False

        return temp

    @is_for_eccentric_bearing.setter
    def is_for_eccentric_bearing(self, value: 'bool'):
        self.wrapped.IsForEccentricBearing = bool(value) if value is not None else False
