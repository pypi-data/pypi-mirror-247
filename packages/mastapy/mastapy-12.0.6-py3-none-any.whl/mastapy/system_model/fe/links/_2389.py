﻿"""_2389.py

ShaftHubConnectionFELink
"""


from mastapy.system_model.fe.links import _2382
from mastapy._internal.python_net import python_net_import

_SHAFT_HUB_CONNECTION_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.FE.Links', 'ShaftHubConnectionFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftHubConnectionFELink',)


class ShaftHubConnectionFELink(_2382.MultiNodeConnectorFELink):
    """ShaftHubConnectionFELink

    This is a mastapy class.
    """

    TYPE = _SHAFT_HUB_CONNECTION_FE_LINK

    def __init__(self, instance_to_wrap: 'ShaftHubConnectionFELink.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
