﻿"""_148.py

TorsionalFrictionNodePair
"""


from mastapy.nodal_analysis.nodal_entities import _133
from mastapy._internal.python_net import python_net_import

_TORSIONAL_FRICTION_NODE_PAIR = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'TorsionalFrictionNodePair')


__docformat__ = 'restructuredtext en'
__all__ = ('TorsionalFrictionNodePair',)


class TorsionalFrictionNodePair(_133.ConcentricConnectionNodalComponent):
    """TorsionalFrictionNodePair

    This is a mastapy class.
    """

    TYPE = _TORSIONAL_FRICTION_NODE_PAIR

    def __init__(self, instance_to_wrap: 'TorsionalFrictionNodePair.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
