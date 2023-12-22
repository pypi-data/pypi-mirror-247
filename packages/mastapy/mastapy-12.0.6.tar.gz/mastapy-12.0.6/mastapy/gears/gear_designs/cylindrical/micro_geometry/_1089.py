﻿"""_1089.py

CylindricalGearLeadModificationAtProfilePosition
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _1018
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1088
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LEAD_MODIFICATION_AT_PROFILE_POSITION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearLeadModificationAtProfilePosition')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLeadModificationAtProfilePosition',)


class CylindricalGearLeadModificationAtProfilePosition(_1088.CylindricalGearLeadModification):
    """CylindricalGearLeadModificationAtProfilePosition

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_LEAD_MODIFICATION_AT_PROFILE_POSITION

    def __init__(self, instance_to_wrap: 'CylindricalGearLeadModificationAtProfilePosition.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def position_on_profile_factor(self) -> 'float':
        """float: 'PositionOnProfileFactor' is the original name of this property."""

        temp = self.wrapped.PositionOnProfileFactor

        if temp is None:
            return 0.0

        return temp

    @position_on_profile_factor.setter
    def position_on_profile_factor(self, value: 'float'):
        self.wrapped.PositionOnProfileFactor = float(value) if value is not None else 0.0

    @property
    def profile_measurement(self) -> '_1018.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ProfileMeasurement' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileMeasurement

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
