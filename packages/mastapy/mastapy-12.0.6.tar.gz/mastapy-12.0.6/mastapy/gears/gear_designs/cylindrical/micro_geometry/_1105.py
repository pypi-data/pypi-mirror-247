﻿"""_1105.py

GearAlignment
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _1018
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_ALIGNMENT = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'GearAlignment')


__docformat__ = 'restructuredtext en'
__all__ = ('GearAlignment',)


class GearAlignment(_0.APIBase):
    """GearAlignment

    This is a mastapy class.
    """

    TYPE = _GEAR_ALIGNMENT

    def __init__(self, instance_to_wrap: 'GearAlignment.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diameter(self) -> 'float':
        """float: 'Diameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Diameter

        if temp is None:
            return 0.0

        return temp

    @property
    def index_of_reference_tooth(self) -> 'int':
        """int: 'IndexOfReferenceTooth' is the original name of this property."""

        temp = self.wrapped.IndexOfReferenceTooth

        if temp is None:
            return 0

        return temp

    @index_of_reference_tooth.setter
    def index_of_reference_tooth(self, value: 'int'):
        self.wrapped.IndexOfReferenceTooth = int(value) if value is not None else 0

    @property
    def radius(self) -> 'float':
        """float: 'Radius' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Radius

        if temp is None:
            return 0.0

        return temp

    @property
    def roll_angle(self) -> 'float':
        """float: 'RollAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollAngle

        if temp is None:
            return 0.0

        return temp

    @property
    def roll_distance(self) -> 'float':
        """float: 'RollDistance' is the original name of this property."""

        temp = self.wrapped.RollDistance

        if temp is None:
            return 0.0

        return temp

    @roll_distance.setter
    def roll_distance(self, value: 'float'):
        self.wrapped.RollDistance = float(value) if value is not None else 0.0

    @property
    def profile_measurement_of_the_tooth_at_least_roll_distance(self) -> '_1018.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'ProfileMeasurementOfTheToothAtLeastRollDistance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileMeasurementOfTheToothAtLeastRollDistance

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
