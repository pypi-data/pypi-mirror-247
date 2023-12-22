﻿"""_2243.py

MountableComponentSocket
"""


from mastapy.system_model.connections_and_sockets import _2235
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'MountableComponentSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentSocket',)


class MountableComponentSocket(_2235.CylindricalSocket):
    """MountableComponentSocket

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_SOCKET

    def __init__(self, instance_to_wrap: 'MountableComponentSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
