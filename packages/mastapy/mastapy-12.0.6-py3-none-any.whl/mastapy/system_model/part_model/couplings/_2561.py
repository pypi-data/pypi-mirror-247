﻿"""_2561.py

SynchroniserPart
"""


from mastapy.system_model.part_model.couplings import _2540
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserPart',)


class SynchroniserPart(_2540.CouplingHalf):
    """SynchroniserPart

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_PART

    def __init__(self, instance_to_wrap: 'SynchroniserPart.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
