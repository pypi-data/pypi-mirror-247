﻿"""_2469.py

AGMAGleasonConicalGear
"""


from mastapy.system_model.part_model.gears import _2479
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGear',)


class AGMAGleasonConicalGear(_2479.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
