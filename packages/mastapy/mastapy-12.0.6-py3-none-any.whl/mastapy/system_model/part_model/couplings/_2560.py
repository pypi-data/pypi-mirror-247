﻿"""_2560.py

SynchroniserHalf
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.part_model.couplings import _2559, _2561
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalf',)


class SynchroniserHalf(_2561.SynchroniserPart):
    """SynchroniserHalf

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_HALF

    def __init__(self, instance_to_wrap: 'SynchroniserHalf.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def area_of_cone_with_minimum_area(self) -> 'float':
        """float: 'AreaOfConeWithMinimumArea' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AreaOfConeWithMinimumArea

        if temp is None:
            return 0.0

        return temp

    @property
    def blocker_chamfer_angle(self) -> 'float':
        """float: 'BlockerChamferAngle' is the original name of this property."""

        temp = self.wrapped.BlockerChamferAngle

        if temp is None:
            return 0.0

        return temp

    @blocker_chamfer_angle.setter
    def blocker_chamfer_angle(self, value: 'float'):
        self.wrapped.BlockerChamferAngle = float(value) if value is not None else 0.0

    @property
    def blocker_chamfer_coefficient_of_friction(self) -> 'float':
        """float: 'BlockerChamferCoefficientOfFriction' is the original name of this property."""

        temp = self.wrapped.BlockerChamferCoefficientOfFriction

        if temp is None:
            return 0.0

        return temp

    @blocker_chamfer_coefficient_of_friction.setter
    def blocker_chamfer_coefficient_of_friction(self, value: 'float'):
        self.wrapped.BlockerChamferCoefficientOfFriction = float(value) if value is not None else 0.0

    @property
    def blocker_chamfer_pcd(self) -> 'float':
        """float: 'BlockerChamferPCD' is the original name of this property."""

        temp = self.wrapped.BlockerChamferPCD

        if temp is None:
            return 0.0

        return temp

    @blocker_chamfer_pcd.setter
    def blocker_chamfer_pcd(self, value: 'float'):
        self.wrapped.BlockerChamferPCD = float(value) if value is not None else 0.0

    @property
    def cone_side(self) -> 'str':
        """str: 'ConeSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConeSide

        if temp is None:
            return ''

        return temp

    @property
    def diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Diameter' is the original name of this property."""

        temp = self.wrapped.Diameter

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @diameter.setter
    def diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Diameter = value

    @property
    def number_of_surfaces(self) -> 'int':
        """int: 'NumberOfSurfaces' is the original name of this property."""

        temp = self.wrapped.NumberOfSurfaces

        if temp is None:
            return 0

        return temp

    @number_of_surfaces.setter
    def number_of_surfaces(self, value: 'int'):
        self.wrapped.NumberOfSurfaces = int(value) if value is not None else 0

    @property
    def total_area_of_cones(self) -> 'float':
        """float: 'TotalAreaOfCones' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalAreaOfCones

        if temp is None:
            return 0.0

        return temp

    @property
    def cones(self) -> 'List[_2559.SynchroniserCone]':
        """List[SynchroniserCone]: 'Cones' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Cones

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
