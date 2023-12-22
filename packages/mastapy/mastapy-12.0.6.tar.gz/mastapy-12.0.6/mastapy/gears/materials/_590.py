﻿"""_590.py

ISOCylindricalGearMaterial
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import list_with_selected_item, overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.materials import _272
from mastapy.gears.materials import _584
from mastapy._internal.python_net import python_net_import

_ISO_CYLINDRICAL_GEAR_MATERIAL = python_net_import('SMT.MastaAPI.Gears.Materials', 'ISOCylindricalGearMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOCylindricalGearMaterial',)


class ISOCylindricalGearMaterial(_584.CylindricalGearMaterial):
    """ISOCylindricalGearMaterial

    This is a mastapy class.
    """

    TYPE = _ISO_CYLINDRICAL_GEAR_MATERIAL

    def __init__(self, instance_to_wrap: 'ISOCylindricalGearMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def limited_pitting_allowed(self) -> 'bool':
        """bool: 'LimitedPittingAllowed' is the original name of this property."""

        temp = self.wrapped.LimitedPittingAllowed

        if temp is None:
            return False

        return temp

    @limited_pitting_allowed.setter
    def limited_pitting_allowed(self, value: 'bool'):
        self.wrapped.LimitedPittingAllowed = bool(value) if value is not None else False

    @property
    def long_life_life_factor_bending(self) -> 'float':
        """float: 'LongLifeLifeFactorBending' is the original name of this property."""

        temp = self.wrapped.LongLifeLifeFactorBending

        if temp is None:
            return 0.0

        return temp

    @long_life_life_factor_bending.setter
    def long_life_life_factor_bending(self, value: 'float'):
        self.wrapped.LongLifeLifeFactorBending = float(value) if value is not None else 0.0

    @property
    def long_life_life_factor_contact(self) -> 'float':
        """float: 'LongLifeLifeFactorContact' is the original name of this property."""

        temp = self.wrapped.LongLifeLifeFactorContact

        if temp is None:
            return 0.0

        return temp

    @long_life_life_factor_contact.setter
    def long_life_life_factor_contact(self, value: 'float'):
        self.wrapped.LongLifeLifeFactorContact = float(value) if value is not None else 0.0

    @property
    def material_has_a_well_defined_yield_point(self) -> 'bool':
        """bool: 'MaterialHasAWellDefinedYieldPoint' is the original name of this property."""

        temp = self.wrapped.MaterialHasAWellDefinedYieldPoint

        if temp is None:
            return False

        return temp

    @material_has_a_well_defined_yield_point.setter
    def material_has_a_well_defined_yield_point(self, value: 'bool'):
        self.wrapped.MaterialHasAWellDefinedYieldPoint = bool(value) if value is not None else False

    @property
    def material_type(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'MaterialType' is the original name of this property."""

        temp = self.wrapped.MaterialType

        if temp is None:
            return ''

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else ''

    @material_type.setter
    def material_type(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.MaterialType = value

    @property
    def n0_bending(self) -> 'float':
        """float: 'N0Bending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.N0Bending

        if temp is None:
            return 0.0

        return temp

    @property
    def n0_contact(self) -> 'float':
        """float: 'N0Contact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.N0Contact

        if temp is None:
            return 0.0

        return temp

    @property
    def proof_stress(self) -> 'float':
        """float: 'ProofStress' is the original name of this property."""

        temp = self.wrapped.ProofStress

        if temp is None:
            return 0.0

        return temp

    @proof_stress.setter
    def proof_stress(self, value: 'float'):
        self.wrapped.ProofStress = float(value) if value is not None else 0.0

    @property
    def quality_grade(self) -> '_272.QualityGrade':
        """QualityGrade: 'QualityGrade' is the original name of this property."""

        temp = self.wrapped.QualityGrade

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_272.QualityGrade)(value) if value is not None else None

    @quality_grade.setter
    def quality_grade(self, value: '_272.QualityGrade'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.QualityGrade = value

    @property
    def shot_peening_bending_stress_benefit(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ShotPeeningBendingStressBenefit' is the original name of this property."""

        temp = self.wrapped.ShotPeeningBendingStressBenefit

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @shot_peening_bending_stress_benefit.setter
    def shot_peening_bending_stress_benefit(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ShotPeeningBendingStressBenefit = value

    @property
    def use_custom_material_for_bending(self) -> 'bool':
        """bool: 'UseCustomMaterialForBending' is the original name of this property."""

        temp = self.wrapped.UseCustomMaterialForBending

        if temp is None:
            return False

        return temp

    @use_custom_material_for_bending.setter
    def use_custom_material_for_bending(self, value: 'bool'):
        self.wrapped.UseCustomMaterialForBending = bool(value) if value is not None else False

    @property
    def use_custom_material_for_contact(self) -> 'bool':
        """bool: 'UseCustomMaterialForContact' is the original name of this property."""

        temp = self.wrapped.UseCustomMaterialForContact

        if temp is None:
            return False

        return temp

    @use_custom_material_for_contact.setter
    def use_custom_material_for_contact(self, value: 'bool'):
        self.wrapped.UseCustomMaterialForContact = bool(value) if value is not None else False

    @property
    def use_iso633652003_material_definitions(self) -> 'bool':
        """bool: 'UseISO633652003MaterialDefinitions' is the original name of this property."""

        temp = self.wrapped.UseISO633652003MaterialDefinitions

        if temp is None:
            return False

        return temp

    @use_iso633652003_material_definitions.setter
    def use_iso633652003_material_definitions(self, value: 'bool'):
        self.wrapped.UseISO633652003MaterialDefinitions = bool(value) if value is not None else False
