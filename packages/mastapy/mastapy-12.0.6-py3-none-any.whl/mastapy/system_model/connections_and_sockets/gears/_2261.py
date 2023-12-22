﻿"""_2261.py

BevelDifferentialGearTeethSocket
"""


from mastapy.system_model.connections_and_sockets.gears import _2263
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_TEETH_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearTeethSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearTeethSocket',)


class BevelDifferentialGearTeethSocket(_2263.BevelGearTeethSocket):
    """BevelDifferentialGearTeethSocket

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_TEETH_SOCKET

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearTeethSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
