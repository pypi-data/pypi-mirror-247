﻿"""_119.py

ElementScalarState
"""


from mastapy.nodal_analysis.states import _120
from mastapy._internal.python_net import python_net_import

_ELEMENT_SCALAR_STATE = python_net_import('SMT.MastaAPI.NodalAnalysis.States', 'ElementScalarState')


__docformat__ = 'restructuredtext en'
__all__ = ('ElementScalarState',)


class ElementScalarState(_120.ElementVectorState):
    """ElementScalarState

    This is a mastapy class.
    """

    TYPE = _ELEMENT_SCALAR_STATE

    def __init__(self, instance_to_wrap: 'ElementScalarState.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
