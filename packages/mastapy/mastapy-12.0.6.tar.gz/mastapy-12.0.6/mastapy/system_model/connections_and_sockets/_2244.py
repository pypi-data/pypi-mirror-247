﻿"""_2244.py

OuterShaftSocket
"""


from mastapy.system_model.connections_and_sockets import _2245
from mastapy._internal.python_net import python_net_import

_OUTER_SHAFT_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'OuterShaftSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('OuterShaftSocket',)


class OuterShaftSocket(_2245.OuterShaftSocketBase):
    """OuterShaftSocket

    This is a mastapy class.
    """

    TYPE = _OUTER_SHAFT_SOCKET

    def __init__(self, instance_to_wrap: 'OuterShaftSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
