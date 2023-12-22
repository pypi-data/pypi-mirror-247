﻿"""_575.py

ProfileModification
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.micro_geometry import (
    _566, _567, _568, _569,
    _570, _571, _573, _574,
    _572
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.math_utility import _1501
from mastapy._internal.python_net import python_net_import

_PROFILE_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'ProfileModification')


__docformat__ = 'restructuredtext en'
__all__ = ('ProfileModification',)


class ProfileModification(_572.Modification):
    """ProfileModification

    This is a mastapy class.
    """

    TYPE = _PROFILE_MODIFICATION

    def __init__(self, instance_to_wrap: 'ProfileModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def barrelling_peak_point_factor(self) -> 'float':
        """float: 'BarrellingPeakPointFactor' is the original name of this property."""

        temp = self.wrapped.BarrellingPeakPointFactor

        if temp is None:
            return 0.0

        return temp

    @barrelling_peak_point_factor.setter
    def barrelling_peak_point_factor(self, value: 'float'):
        self.wrapped.BarrellingPeakPointFactor = float(value) if value is not None else 0.0

    @property
    def barrelling_relief(self) -> 'float':
        """float: 'BarrellingRelief' is the original name of this property."""

        temp = self.wrapped.BarrellingRelief

        if temp is None:
            return 0.0

        return temp

    @barrelling_relief.setter
    def barrelling_relief(self, value: 'float'):
        self.wrapped.BarrellingRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_lower_limit_factor(self) -> 'float':
        """float: 'EvaluationLowerLimitFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_factor.setter
    def evaluation_lower_limit_factor(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_lower_limit_factor_for_zero_root_relief(self) -> 'float':
        """float: 'EvaluationLowerLimitFactorForZeroRootRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationLowerLimitFactorForZeroRootRelief

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_factor_for_zero_root_relief.setter
    def evaluation_lower_limit_factor_for_zero_root_relief(self, value: 'float'):
        self.wrapped.EvaluationLowerLimitFactorForZeroRootRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_upper_limit_factor(self) -> 'float':
        """float: 'EvaluationUpperLimitFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_factor.setter
    def evaluation_upper_limit_factor(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_upper_limit_factor_for_zero_tip_relief(self) -> 'float':
        """float: 'EvaluationUpperLimitFactorForZeroTipRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationUpperLimitFactorForZeroTipRelief

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_factor_for_zero_tip_relief.setter
    def evaluation_upper_limit_factor_for_zero_tip_relief(self, value: 'float'):
        self.wrapped.EvaluationUpperLimitFactorForZeroTipRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_of_linear_root_relief_factor(self) -> 'float':
        """float: 'EvaluationOfLinearRootReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearRootReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_root_relief_factor.setter
    def evaluation_of_linear_root_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfLinearRootReliefFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_linear_tip_relief_factor(self) -> 'float':
        """float: 'EvaluationOfLinearTipReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearTipReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_tip_relief_factor.setter
    def evaluation_of_linear_tip_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfLinearTipReliefFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_parabolic_root_relief_factor(self) -> 'float':
        """float: 'EvaluationOfParabolicRootReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicRootReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_root_relief_factor.setter
    def evaluation_of_parabolic_root_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicRootReliefFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_parabolic_tip_relief_factor(self) -> 'float':
        """float: 'EvaluationOfParabolicTipReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicTipReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_tip_relief_factor.setter
    def evaluation_of_parabolic_tip_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicTipReliefFactor = float(value) if value is not None else 0.0

    @property
    def linear_relief(self) -> 'float':
        """float: 'LinearRelief' is the original name of this property."""

        temp = self.wrapped.LinearRelief

        if temp is None:
            return 0.0

        return temp

    @linear_relief.setter
    def linear_relief(self, value: 'float'):
        self.wrapped.LinearRelief = float(value) if value is not None else 0.0

    @property
    def linear_root_relief(self) -> 'float':
        """float: 'LinearRootRelief' is the original name of this property."""

        temp = self.wrapped.LinearRootRelief

        if temp is None:
            return 0.0

        return temp

    @linear_root_relief.setter
    def linear_root_relief(self, value: 'float'):
        self.wrapped.LinearRootRelief = float(value) if value is not None else 0.0

    @property
    def linear_tip_relief(self) -> 'float':
        """float: 'LinearTipRelief' is the original name of this property."""

        temp = self.wrapped.LinearTipRelief

        if temp is None:
            return 0.0

        return temp

    @linear_tip_relief.setter
    def linear_tip_relief(self, value: 'float'):
        self.wrapped.LinearTipRelief = float(value) if value is not None else 0.0

    @property
    def location_of_evaluation_lower_limit(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit: 'LocationOfEvaluationLowerLimit' is the original name of this property."""

        temp = self.wrapped.LocationOfEvaluationLowerLimit

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_evaluation_lower_limit.setter
    def location_of_evaluation_lower_limit(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfEvaluationLowerLimit = value

    @property
    def location_of_evaluation_lower_limit_for_zero_root_relief(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit: 'LocationOfEvaluationLowerLimitForZeroRootRelief' is the original name of this property."""

        temp = self.wrapped.LocationOfEvaluationLowerLimitForZeroRootRelief

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_evaluation_lower_limit_for_zero_root_relief.setter
    def location_of_evaluation_lower_limit_for_zero_root_relief(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfEvaluationLowerLimitForZeroRootRelief = value

    @property
    def location_of_evaluation_upper_limit(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit: 'LocationOfEvaluationUpperLimit' is the original name of this property."""

        temp = self.wrapped.LocationOfEvaluationUpperLimit

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_evaluation_upper_limit.setter
    def location_of_evaluation_upper_limit(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfEvaluationUpperLimit = value

    @property
    def location_of_evaluation_upper_limit_for_zero_tip_relief(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit: 'LocationOfEvaluationUpperLimitForZeroTipRelief' is the original name of this property."""

        temp = self.wrapped.LocationOfEvaluationUpperLimitForZeroTipRelief

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_evaluation_upper_limit_for_zero_tip_relief.setter
    def location_of_evaluation_upper_limit_for_zero_tip_relief(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfEvaluationUpperLimitForZeroTipRelief = value

    @property
    def location_of_root_modification_start(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation: 'LocationOfRootModificationStart' is the original name of this property."""

        temp = self.wrapped.LocationOfRootModificationStart

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_root_modification_start.setter
    def location_of_root_modification_start(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfRootModificationStart = value

    @property
    def location_of_root_relief_evaluation(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation: 'LocationOfRootReliefEvaluation' is the original name of this property."""

        temp = self.wrapped.LocationOfRootReliefEvaluation

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_root_relief_evaluation.setter
    def location_of_root_relief_evaluation(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfRootReliefEvaluation = value

    @property
    def location_of_tip_relief_evaluation(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation: 'LocationOfTipReliefEvaluation' is the original name of this property."""

        temp = self.wrapped.LocationOfTipReliefEvaluation

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_tip_relief_evaluation.setter
    def location_of_tip_relief_evaluation(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfTipReliefEvaluation = value

    @property
    def location_of_tip_relief_start(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation':
        """enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation: 'LocationOfTipReliefStart' is the original name of this property."""

        temp = self.wrapped.LocationOfTipReliefStart

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @location_of_tip_relief_start.setter
    def location_of_tip_relief_start(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LocationOfTipReliefStart = value

    @property
    def main_profile_modification_ends_at_the_start_of_root_relief(self) -> '_570.MainProfileReliefEndsAtTheStartOfRootReliefOption':
        """MainProfileReliefEndsAtTheStartOfRootReliefOption: 'MainProfileModificationEndsAtTheStartOfRootRelief' is the original name of this property."""

        temp = self.wrapped.MainProfileModificationEndsAtTheStartOfRootRelief

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_570.MainProfileReliefEndsAtTheStartOfRootReliefOption)(value) if value is not None else None

    @main_profile_modification_ends_at_the_start_of_root_relief.setter
    def main_profile_modification_ends_at_the_start_of_root_relief(self, value: '_570.MainProfileReliefEndsAtTheStartOfRootReliefOption'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MainProfileModificationEndsAtTheStartOfRootRelief = value

    @property
    def main_profile_modification_ends_at_the_start_of_tip_relief(self) -> '_571.MainProfileReliefEndsAtTheStartOfTipReliefOption':
        """MainProfileReliefEndsAtTheStartOfTipReliefOption: 'MainProfileModificationEndsAtTheStartOfTipRelief' is the original name of this property."""

        temp = self.wrapped.MainProfileModificationEndsAtTheStartOfTipRelief

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_571.MainProfileReliefEndsAtTheStartOfTipReliefOption)(value) if value is not None else None

    @main_profile_modification_ends_at_the_start_of_tip_relief.setter
    def main_profile_modification_ends_at_the_start_of_tip_relief(self, value: '_571.MainProfileReliefEndsAtTheStartOfTipReliefOption'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.MainProfileModificationEndsAtTheStartOfTipRelief = value

    @property
    def measure_root_reliefs_from_extrapolated_linear_relief(self) -> 'bool':
        """bool: 'MeasureRootReliefsFromExtrapolatedLinearRelief' is the original name of this property."""

        temp = self.wrapped.MeasureRootReliefsFromExtrapolatedLinearRelief

        if temp is None:
            return False

        return temp

    @measure_root_reliefs_from_extrapolated_linear_relief.setter
    def measure_root_reliefs_from_extrapolated_linear_relief(self, value: 'bool'):
        self.wrapped.MeasureRootReliefsFromExtrapolatedLinearRelief = bool(value) if value is not None else False

    @property
    def measure_tip_reliefs_from_extrapolated_linear_relief(self) -> 'bool':
        """bool: 'MeasureTipReliefsFromExtrapolatedLinearRelief' is the original name of this property."""

        temp = self.wrapped.MeasureTipReliefsFromExtrapolatedLinearRelief

        if temp is None:
            return False

        return temp

    @measure_tip_reliefs_from_extrapolated_linear_relief.setter
    def measure_tip_reliefs_from_extrapolated_linear_relief(self, value: 'bool'):
        self.wrapped.MeasureTipReliefsFromExtrapolatedLinearRelief = bool(value) if value is not None else False

    @property
    def measured_data(self) -> '_1501.Vector2DListAccessor':
        """Vector2DListAccessor: 'MeasuredData' is the original name of this property."""

        temp = self.wrapped.MeasuredData

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measured_data.setter
    def measured_data(self, value: '_1501.Vector2DListAccessor'):
        self.wrapped.MeasuredData = value

    @property
    def parabolic_root_relief(self) -> 'float':
        """float: 'ParabolicRootRelief' is the original name of this property."""

        temp = self.wrapped.ParabolicRootRelief

        if temp is None:
            return 0.0

        return temp

    @parabolic_root_relief.setter
    def parabolic_root_relief(self, value: 'float'):
        self.wrapped.ParabolicRootRelief = float(value) if value is not None else 0.0

    @property
    def parabolic_root_relief_starts_tangent_to_main_profile_relief(self) -> '_573.ParabolicRootReliefStartsTangentToMainProfileRelief':
        """ParabolicRootReliefStartsTangentToMainProfileRelief: 'ParabolicRootReliefStartsTangentToMainProfileRelief' is the original name of this property."""

        temp = self.wrapped.ParabolicRootReliefStartsTangentToMainProfileRelief

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_573.ParabolicRootReliefStartsTangentToMainProfileRelief)(value) if value is not None else None

    @parabolic_root_relief_starts_tangent_to_main_profile_relief.setter
    def parabolic_root_relief_starts_tangent_to_main_profile_relief(self, value: '_573.ParabolicRootReliefStartsTangentToMainProfileRelief'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ParabolicRootReliefStartsTangentToMainProfileRelief = value

    @property
    def parabolic_tip_relief(self) -> 'float':
        """float: 'ParabolicTipRelief' is the original name of this property."""

        temp = self.wrapped.ParabolicTipRelief

        if temp is None:
            return 0.0

        return temp

    @parabolic_tip_relief.setter
    def parabolic_tip_relief(self, value: 'float'):
        self.wrapped.ParabolicTipRelief = float(value) if value is not None else 0.0

    @property
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief(self) -> '_574.ParabolicTipReliefStartsTangentToMainProfileRelief':
        """ParabolicTipReliefStartsTangentToMainProfileRelief: 'ParabolicTipReliefStartsTangentToMainProfileRelief' is the original name of this property."""

        temp = self.wrapped.ParabolicTipReliefStartsTangentToMainProfileRelief

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_574.ParabolicTipReliefStartsTangentToMainProfileRelief)(value) if value is not None else None

    @parabolic_tip_relief_starts_tangent_to_main_profile_relief.setter
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief(self, value: '_574.ParabolicTipReliefStartsTangentToMainProfileRelief'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ParabolicTipReliefStartsTangentToMainProfileRelief = value

    @property
    def start_of_linear_root_relief_factor(self) -> 'float':
        """float: 'StartOfLinearRootReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfLinearRootReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_root_relief_factor.setter
    def start_of_linear_root_relief_factor(self, value: 'float'):
        self.wrapped.StartOfLinearRootReliefFactor = float(value) if value is not None else 0.0

    @property
    def start_of_linear_tip_relief_factor(self) -> 'float':
        """float: 'StartOfLinearTipReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfLinearTipReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_tip_relief_factor.setter
    def start_of_linear_tip_relief_factor(self, value: 'float'):
        self.wrapped.StartOfLinearTipReliefFactor = float(value) if value is not None else 0.0

    @property
    def start_of_parabolic_root_relief_factor(self) -> 'float':
        """float: 'StartOfParabolicRootReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicRootReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_root_relief_factor.setter
    def start_of_parabolic_root_relief_factor(self, value: 'float'):
        self.wrapped.StartOfParabolicRootReliefFactor = float(value) if value is not None else 0.0

    @property
    def start_of_parabolic_tip_relief_factor(self) -> 'float':
        """float: 'StartOfParabolicTipReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicTipReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_tip_relief_factor.setter
    def start_of_parabolic_tip_relief_factor(self, value: 'float'):
        self.wrapped.StartOfParabolicTipReliefFactor = float(value) if value is not None else 0.0

    @property
    def use_measured_data(self) -> 'bool':
        """bool: 'UseMeasuredData' is the original name of this property."""

        temp = self.wrapped.UseMeasuredData

        if temp is None:
            return False

        return temp

    @use_measured_data.setter
    def use_measured_data(self, value: 'bool'):
        self.wrapped.UseMeasuredData = bool(value) if value is not None else False

    @property
    def use_user_specified_barrelling_peak_point(self) -> 'bool':
        """bool: 'UseUserSpecifiedBarrellingPeakPoint' is the original name of this property."""

        temp = self.wrapped.UseUserSpecifiedBarrellingPeakPoint

        if temp is None:
            return False

        return temp

    @use_user_specified_barrelling_peak_point.setter
    def use_user_specified_barrelling_peak_point(self, value: 'bool'):
        self.wrapped.UseUserSpecifiedBarrellingPeakPoint = bool(value) if value is not None else False
