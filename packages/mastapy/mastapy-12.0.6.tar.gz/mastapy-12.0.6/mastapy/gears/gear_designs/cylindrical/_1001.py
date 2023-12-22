﻿"""_1001.py

CylindricalGearBasicRack
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.cylindrical import (
    _993, _1073, _1016, _999
)
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_BASIC_RACK = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearBasicRack')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearBasicRack',)


class CylindricalGearBasicRack(_999.CylindricalGearAbstractRack):
    """CylindricalGearBasicRack

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_BASIC_RACK

    def __init__(self, instance_to_wrap: 'CylindricalGearBasicRack.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def basic_rack_clearance_factor(self) -> 'float':
        """float: 'BasicRackClearanceFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicRackClearanceFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_rack_profile(self) -> '_993.BasicRackProfiles':
        """BasicRackProfiles: 'BasicRackProfile' is the original name of this property."""

        temp = self.wrapped.BasicRackProfile

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_993.BasicRackProfiles)(value) if value is not None else None

    @basic_rack_profile.setter
    def basic_rack_profile(self, value: '_993.BasicRackProfiles'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BasicRackProfile = value

    @property
    def proportional_method_for_tip_clearance(self) -> '_1073.TipAlterationCoefficientMethod':
        """TipAlterationCoefficientMethod: 'ProportionalMethodForTipClearance' is the original name of this property."""

        temp = self.wrapped.ProportionalMethodForTipClearance

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1073.TipAlterationCoefficientMethod)(value) if value is not None else None

    @proportional_method_for_tip_clearance.setter
    def proportional_method_for_tip_clearance(self, value: '_1073.TipAlterationCoefficientMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProportionalMethodForTipClearance = value

    @property
    def tip_alteration_proportional_method_mesh(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'TipAlterationProportionalMethodMesh' is the original name of this property."""

        temp = self.wrapped.TipAlterationProportionalMethodMesh

        if temp is None:
            return ''

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else ''

    @tip_alteration_proportional_method_mesh.setter
    def tip_alteration_proportional_method_mesh(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.TipAlterationProportionalMethodMesh = value

    @property
    def pinion_type_cutter_for_rating(self) -> '_1016.CylindricalGearPinionTypeCutter':
        """CylindricalGearPinionTypeCutter: 'PinionTypeCutterForRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PinionTypeCutterForRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
