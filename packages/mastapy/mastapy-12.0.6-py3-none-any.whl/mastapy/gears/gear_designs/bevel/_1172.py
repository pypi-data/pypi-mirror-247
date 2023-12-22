﻿"""_1172.py

BevelGearSetDesign
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.gear_designs.conical import _1141
from mastapy.math_utility import _1485
from mastapy._internal.implicit import overridable, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.bevel import _1181, _1179, _1180
from mastapy.gears import _341
from mastapy.gears.gear_designs.agma_gleason_conical import _1185
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Bevel', 'BevelGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGearSetDesign',)


class BevelGearSetDesign(_1185.AGMAGleasonConicalGearSetDesign):
    """BevelGearSetDesign

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_SET_DESIGN

    def __init__(self, instance_to_wrap: 'BevelGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_scoring_index(self) -> 'float':
        """float: 'AllowableScoringIndex' is the original name of this property."""

        temp = self.wrapped.AllowableScoringIndex

        if temp is None:
            return 0.0

        return temp

    @allowable_scoring_index.setter
    def allowable_scoring_index(self, value: 'float'):
        self.wrapped.AllowableScoringIndex = float(value) if value is not None else 0.0

    @property
    def backlash_distribution_rule(self) -> '_1141.BacklashDistributionRule':
        """BacklashDistributionRule: 'BacklashDistributionRule' is the original name of this property."""

        temp = self.wrapped.BacklashDistributionRule

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1141.BacklashDistributionRule)(value) if value is not None else None

    @backlash_distribution_rule.setter
    def backlash_distribution_rule(self, value: '_1141.BacklashDistributionRule'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BacklashDistributionRule = value

    @property
    def backlash_used_for_tooth_thickness_calculation(self) -> '_1485.MaxMinMean':
        """MaxMinMean: 'BacklashUsedForToothThicknessCalculation' is the original name of this property."""

        temp = self.wrapped.BacklashUsedForToothThicknessCalculation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1485.MaxMinMean)(value) if value is not None else None

    @backlash_used_for_tooth_thickness_calculation.setter
    def backlash_used_for_tooth_thickness_calculation(self, value: '_1485.MaxMinMean'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BacklashUsedForToothThicknessCalculation = value

    @property
    def basic_crown_gear_addendum_factor(self) -> 'float':
        """float: 'BasicCrownGearAddendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicCrownGearAddendumFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_crown_gear_dedendum_factor(self) -> 'float':
        """float: 'BasicCrownGearDedendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicCrownGearDedendumFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def circular_thickness_factor(self) -> 'float':
        """float: 'CircularThicknessFactor' is the original name of this property."""

        temp = self.wrapped.CircularThicknessFactor

        if temp is None:
            return 0.0

        return temp

    @circular_thickness_factor.setter
    def circular_thickness_factor(self, value: 'float'):
        self.wrapped.CircularThicknessFactor = float(value) if value is not None else 0.0

    @property
    def clearance(self) -> 'float':
        """float: 'Clearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clearance

        if temp is None:
            return 0.0

        return temp

    @property
    def diametral_pitch(self) -> 'float':
        """float: 'DiametralPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DiametralPitch

        if temp is None:
            return 0.0

        return temp

    @property
    def factor_of_safety_for_scoring(self) -> 'float':
        """float: 'FactorOfSafetyForScoring' is the original name of this property."""

        temp = self.wrapped.FactorOfSafetyForScoring

        if temp is None:
            return 0.0

        return temp

    @factor_of_safety_for_scoring.setter
    def factor_of_safety_for_scoring(self, value: 'float'):
        self.wrapped.FactorOfSafetyForScoring = float(value) if value is not None else 0.0

    @property
    def ideal_circular_thickness_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'IdealCircularThicknessFactor' is the original name of this property."""

        temp = self.wrapped.IdealCircularThicknessFactor

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @ideal_circular_thickness_factor.setter
    def ideal_circular_thickness_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.IdealCircularThicknessFactor = value

    @property
    def ideal_pinion_mean_transverse_circular_thickness(self) -> 'float':
        """float: 'IdealPinionMeanTransverseCircularThickness' is the original name of this property."""

        temp = self.wrapped.IdealPinionMeanTransverseCircularThickness

        if temp is None:
            return 0.0

        return temp

    @ideal_pinion_mean_transverse_circular_thickness.setter
    def ideal_pinion_mean_transverse_circular_thickness(self, value: 'float'):
        self.wrapped.IdealPinionMeanTransverseCircularThickness = float(value) if value is not None else 0.0

    @property
    def ideal_pinion_outer_transverse_circular_thickness(self) -> 'float':
        """float: 'IdealPinionOuterTransverseCircularThickness' is the original name of this property."""

        temp = self.wrapped.IdealPinionOuterTransverseCircularThickness

        if temp is None:
            return 0.0

        return temp

    @ideal_pinion_outer_transverse_circular_thickness.setter
    def ideal_pinion_outer_transverse_circular_thickness(self, value: 'float'):
        self.wrapped.IdealPinionOuterTransverseCircularThickness = float(value) if value is not None else 0.0

    @property
    def ideal_wheel_finish_cutter_point_width(self) -> 'float':
        """float: 'IdealWheelFinishCutterPointWidth' is the original name of this property."""

        temp = self.wrapped.IdealWheelFinishCutterPointWidth

        if temp is None:
            return 0.0

        return temp

    @ideal_wheel_finish_cutter_point_width.setter
    def ideal_wheel_finish_cutter_point_width(self, value: 'float'):
        self.wrapped.IdealWheelFinishCutterPointWidth = float(value) if value is not None else 0.0

    @property
    def ideal_wheel_mean_slot_width(self) -> 'float':
        """float: 'IdealWheelMeanSlotWidth' is the original name of this property."""

        temp = self.wrapped.IdealWheelMeanSlotWidth

        if temp is None:
            return 0.0

        return temp

    @ideal_wheel_mean_slot_width.setter
    def ideal_wheel_mean_slot_width(self, value: 'float'):
        self.wrapped.IdealWheelMeanSlotWidth = float(value) if value is not None else 0.0

    @property
    def mean_addendum_factor(self) -> 'float':
        """float: 'MeanAddendumFactor' is the original name of this property."""

        temp = self.wrapped.MeanAddendumFactor

        if temp is None:
            return 0.0

        return temp

    @mean_addendum_factor.setter
    def mean_addendum_factor(self, value: 'float'):
        self.wrapped.MeanAddendumFactor = float(value) if value is not None else 0.0

    @property
    def mean_circular_pitch(self) -> 'float':
        """float: 'MeanCircularPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanCircularPitch

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_clearance_factor(self) -> 'float':
        """float: 'MeanClearanceFactor' is the original name of this property."""

        temp = self.wrapped.MeanClearanceFactor

        if temp is None:
            return 0.0

        return temp

    @mean_clearance_factor.setter
    def mean_clearance_factor(self, value: 'float'):
        self.wrapped.MeanClearanceFactor = float(value) if value is not None else 0.0

    @property
    def mean_depth_factor(self) -> 'float':
        """float: 'MeanDepthFactor' is the original name of this property."""

        temp = self.wrapped.MeanDepthFactor

        if temp is None:
            return 0.0

        return temp

    @mean_depth_factor.setter
    def mean_depth_factor(self, value: 'float'):
        self.wrapped.MeanDepthFactor = float(value) if value is not None else 0.0

    @property
    def mean_diametral_pitch(self) -> 'float':
        """float: 'MeanDiametralPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanDiametralPitch

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_whole_depth(self) -> 'float':
        """float: 'MeanWholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanWholeDepth

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_working_depth(self) -> 'float':
        """float: 'MeanWorkingDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeanWorkingDepth

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_number_of_teeth_for_recommended_tooth_proportions(self) -> 'int':
        """int: 'MinimumNumberOfTeethForRecommendedToothProportions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumNumberOfTeethForRecommendedToothProportions

        if temp is None:
            return 0

        return temp

    @property
    def outer_wheel_addendum(self) -> 'float':
        """float: 'OuterWheelAddendum' is the original name of this property."""

        temp = self.wrapped.OuterWheelAddendum

        if temp is None:
            return 0.0

        return temp

    @outer_wheel_addendum.setter
    def outer_wheel_addendum(self, value: 'float'):
        self.wrapped.OuterWheelAddendum = float(value) if value is not None else 0.0

    @property
    def outer_whole_depth(self) -> 'float':
        """float: 'OuterWholeDepth' is the original name of this property."""

        temp = self.wrapped.OuterWholeDepth

        if temp is None:
            return 0.0

        return temp

    @outer_whole_depth.setter
    def outer_whole_depth(self, value: 'float'):
        self.wrapped.OuterWholeDepth = float(value) if value is not None else 0.0

    @property
    def outer_working_depth(self) -> 'float':
        """float: 'OuterWorkingDepth' is the original name of this property."""

        temp = self.wrapped.OuterWorkingDepth

        if temp is None:
            return 0.0

        return temp

    @outer_working_depth.setter
    def outer_working_depth(self, value: 'float'):
        self.wrapped.OuterWorkingDepth = float(value) if value is not None else 0.0

    @property
    def pressure_angle(self) -> 'float':
        """float: 'PressureAngle' is the original name of this property."""

        temp = self.wrapped.PressureAngle

        if temp is None:
            return 0.0

        return temp

    @pressure_angle.setter
    def pressure_angle(self, value: 'float'):
        self.wrapped.PressureAngle = float(value) if value is not None else 0.0

    @property
    def profile_shift_coefficient(self) -> 'float':
        """float: 'ProfileShiftCoefficient' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileShiftCoefficient

        if temp is None:
            return 0.0

        return temp

    @property
    def round_cutter_specifications(self) -> '_1181.WheelFinishCutterPointWidthRestrictionMethod':
        """WheelFinishCutterPointWidthRestrictionMethod: 'RoundCutterSpecifications' is the original name of this property."""

        temp = self.wrapped.RoundCutterSpecifications

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1181.WheelFinishCutterPointWidthRestrictionMethod)(value) if value is not None else None

    @round_cutter_specifications.setter
    def round_cutter_specifications(self, value: '_1181.WheelFinishCutterPointWidthRestrictionMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RoundCutterSpecifications = value

    @property
    def specified_pinion_dedendum_angle(self) -> 'float':
        """float: 'SpecifiedPinionDedendumAngle' is the original name of this property."""

        temp = self.wrapped.SpecifiedPinionDedendumAngle

        if temp is None:
            return 0.0

        return temp

    @specified_pinion_dedendum_angle.setter
    def specified_pinion_dedendum_angle(self, value: 'float'):
        self.wrapped.SpecifiedPinionDedendumAngle = float(value) if value is not None else 0.0

    @property
    def specified_wheel_dedendum_angle(self) -> 'float':
        """float: 'SpecifiedWheelDedendumAngle' is the original name of this property."""

        temp = self.wrapped.SpecifiedWheelDedendumAngle

        if temp is None:
            return 0.0

        return temp

    @specified_wheel_dedendum_angle.setter
    def specified_wheel_dedendum_angle(self, value: 'float'):
        self.wrapped.SpecifiedWheelDedendumAngle = float(value) if value is not None else 0.0

    @property
    def strength_factor(self) -> 'float':
        """float: 'StrengthFactor' is the original name of this property."""

        temp = self.wrapped.StrengthFactor

        if temp is None:
            return 0.0

        return temp

    @strength_factor.setter
    def strength_factor(self, value: 'float'):
        self.wrapped.StrengthFactor = float(value) if value is not None else 0.0

    @property
    def thickness_modification_coefficient_theoretical(self) -> 'float':
        """float: 'ThicknessModificationCoefficientTheoretical' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThicknessModificationCoefficientTheoretical

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_proportions_input_method(self) -> '_1179.ToothProportionsInputMethod':
        """ToothProportionsInputMethod: 'ToothProportionsInputMethod' is the original name of this property."""

        temp = self.wrapped.ToothProportionsInputMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1179.ToothProportionsInputMethod)(value) if value is not None else None

    @tooth_proportions_input_method.setter
    def tooth_proportions_input_method(self, value: '_1179.ToothProportionsInputMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToothProportionsInputMethod = value

    @property
    def tooth_taper_root_line_tilt_method(self) -> '_341.SpiralBevelRootLineTilt':
        """SpiralBevelRootLineTilt: 'ToothTaperRootLineTiltMethod' is the original name of this property."""

        temp = self.wrapped.ToothTaperRootLineTiltMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_341.SpiralBevelRootLineTilt)(value) if value is not None else None

    @tooth_taper_root_line_tilt_method.setter
    def tooth_taper_root_line_tilt_method(self, value: '_341.SpiralBevelRootLineTilt'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ToothTaperRootLineTiltMethod = value

    @property
    def tooth_thickness_specification_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod: 'ToothThicknessSpecificationMethod' is the original name of this property."""

        temp = self.wrapped.ToothThicknessSpecificationMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @tooth_thickness_specification_method.setter
    def tooth_thickness_specification_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ToothThicknessSpecificationMethod = value

    @property
    def use_recommended_tooth_proportions(self) -> 'bool':
        """bool: 'UseRecommendedToothProportions' is the original name of this property."""

        temp = self.wrapped.UseRecommendedToothProportions

        if temp is None:
            return False

        return temp

    @use_recommended_tooth_proportions.setter
    def use_recommended_tooth_proportions(self, value: 'bool'):
        self.wrapped.UseRecommendedToothProportions = bool(value) if value is not None else False

    @property
    def wheel_addendum_factor(self) -> 'float':
        """float: 'WheelAddendumFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelAddendumFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_addendum_multiplier(self) -> 'float':
        """float: 'WheelAddendumMultiplier' is the original name of this property."""

        temp = self.wrapped.WheelAddendumMultiplier

        if temp is None:
            return 0.0

        return temp

    @wheel_addendum_multiplier.setter
    def wheel_addendum_multiplier(self, value: 'float'):
        self.wrapped.WheelAddendumMultiplier = float(value) if value is not None else 0.0

    @property
    def wheel_finish_cutter_point_width(self) -> 'float':
        """float: 'WheelFinishCutterPointWidth' is the original name of this property."""

        temp = self.wrapped.WheelFinishCutterPointWidth

        if temp is None:
            return 0.0

        return temp

    @wheel_finish_cutter_point_width.setter
    def wheel_finish_cutter_point_width(self, value: 'float'):
        self.wrapped.WheelFinishCutterPointWidth = float(value) if value is not None else 0.0

    @property
    def wheel_inner_spiral_angle(self) -> 'float':
        """float: 'WheelInnerSpiralAngle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelInnerSpiralAngle

        if temp is None:
            return 0.0

        return temp

    @property
    def whole_depth_factor(self) -> 'float':
        """float: 'WholeDepthFactor' is the original name of this property."""

        temp = self.wrapped.WholeDepthFactor

        if temp is None:
            return 0.0

        return temp

    @whole_depth_factor.setter
    def whole_depth_factor(self, value: 'float'):
        self.wrapped.WholeDepthFactor = float(value) if value is not None else 0.0

    @property
    def working_depth_factor(self) -> 'float':
        """float: 'WorkingDepthFactor' is the original name of this property."""

        temp = self.wrapped.WorkingDepthFactor

        if temp is None:
            return 0.0

        return temp

    @working_depth_factor.setter
    def working_depth_factor(self, value: 'float'):
        self.wrapped.WorkingDepthFactor = float(value) if value is not None else 0.0

    @property
    def mean_spiral_angle(self) -> 'float':
        """float: 'MeanSpiralAngle' is the original name of this property."""

        temp = self.wrapped.MeanSpiralAngle

        if temp is None:
            return 0.0

        return temp

    @mean_spiral_angle.setter
    def mean_spiral_angle(self, value: 'float'):
        self.wrapped.MeanSpiralAngle = float(value) if value is not None else 0.0

    @property
    def transverse_circular_thickness_factor(self) -> 'float':
        """float: 'TransverseCircularThicknessFactor' is the original name of this property."""

        temp = self.wrapped.TransverseCircularThicknessFactor

        if temp is None:
            return 0.0

        return temp

    @transverse_circular_thickness_factor.setter
    def transverse_circular_thickness_factor(self, value: 'float'):
        self.wrapped.TransverseCircularThicknessFactor = float(value) if value is not None else 0.0
