﻿"""_2505.py

StraightBevelPlanetGear
"""


from mastapy.gears import _334
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2501
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGear',)


class StraightBevelPlanetGear(_2501.StraightBevelDiffGear):
    """StraightBevelPlanetGear

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGear.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetary_details(self) -> '_334.PlanetaryDetail':
        """PlanetaryDetail: 'PlanetaryDetails' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetaryDetails

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
