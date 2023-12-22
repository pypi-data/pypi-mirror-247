﻿"""_2310.py

SpringDamperSocket
"""


from mastapy.system_model.connections_and_sockets.couplings import _2306
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperSocket')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperSocket',)


class SpringDamperSocket(_2306.CouplingSocket):
    """SpringDamperSocket

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_SOCKET

    def __init__(self, instance_to_wrap: 'SpringDamperSocket.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
