﻿"""_954.py

StraightBevelGearDesign
"""


from mastapy.gears.gear_designs.bevel import _1170
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.StraightBevel', 'StraightBevelGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearDesign',)


class StraightBevelGearDesign(_1170.BevelGearDesign):
    """StraightBevelGearDesign

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_GEAR_DESIGN

    def __init__(self, instance_to_wrap: 'StraightBevelGearDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
