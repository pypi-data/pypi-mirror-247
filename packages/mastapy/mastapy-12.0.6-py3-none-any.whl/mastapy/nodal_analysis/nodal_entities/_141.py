﻿"""_141.py

NodalComponent
"""


from mastapy.nodal_analysis.nodal_entities import _143
from mastapy._internal.python_net import python_net_import

_NODAL_COMPONENT = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'NodalComponent')


__docformat__ = 'restructuredtext en'
__all__ = ('NodalComponent',)


class NodalComponent(_143.NodalEntity):
    """NodalComponent

    This is a mastapy class.
    """

    TYPE = _NODAL_COMPONENT

    def __init__(self, instance_to_wrap: 'NodalComponent.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
