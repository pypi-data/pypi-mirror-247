﻿"""_87.py

TransientSolverOptions
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import (
    _56, _71, _82, _89
)
from mastapy._internal.implicit import enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TRANSIENT_SOLVER_OPTIONS = python_net_import('SMT.MastaAPI.NodalAnalysis', 'TransientSolverOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('TransientSolverOptions',)


class TransientSolverOptions(_0.APIBase):
    """TransientSolverOptions

    This is a mastapy class.
    """

    TYPE = _TRANSIENT_SOLVER_OPTIONS

    def __init__(self, instance_to_wrap: 'TransientSolverOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def absolute_tolerance_angular_velocity_for_newton_raphson(self) -> 'float':
        """float: 'AbsoluteToleranceAngularVelocityForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceAngularVelocityForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_angular_velocity_for_newton_raphson.setter
    def absolute_tolerance_angular_velocity_for_newton_raphson(self, value: 'float'):
        self.wrapped.AbsoluteToleranceAngularVelocityForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_angular_velocity_for_step(self) -> 'float':
        """float: 'AbsoluteToleranceAngularVelocityForStep' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceAngularVelocityForStep

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_angular_velocity_for_step.setter
    def absolute_tolerance_angular_velocity_for_step(self, value: 'float'):
        self.wrapped.AbsoluteToleranceAngularVelocityForStep = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_lagrange_force_for_newton_raphson(self) -> 'float':
        """float: 'AbsoluteToleranceLagrangeForceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceLagrangeForceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_lagrange_force_for_newton_raphson.setter
    def absolute_tolerance_lagrange_force_for_newton_raphson(self, value: 'float'):
        self.wrapped.AbsoluteToleranceLagrangeForceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_lagrange_moment_for_newton_raphson(self) -> 'float':
        """float: 'AbsoluteToleranceLagrangeMomentForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceLagrangeMomentForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_lagrange_moment_for_newton_raphson.setter
    def absolute_tolerance_lagrange_moment_for_newton_raphson(self, value: 'float'):
        self.wrapped.AbsoluteToleranceLagrangeMomentForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_simple(self) -> 'float':
        """float: 'AbsoluteToleranceSimple' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceSimple

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_simple.setter
    def absolute_tolerance_simple(self, value: 'float'):
        self.wrapped.AbsoluteToleranceSimple = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_temperature_for_newton_raphson(self) -> 'float':
        """float: 'AbsoluteToleranceTemperatureForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceTemperatureForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_temperature_for_newton_raphson.setter
    def absolute_tolerance_temperature_for_newton_raphson(self, value: 'float'):
        self.wrapped.AbsoluteToleranceTemperatureForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_temperature_for_step(self) -> 'float':
        """float: 'AbsoluteToleranceTemperatureForStep' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceTemperatureForStep

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_temperature_for_step.setter
    def absolute_tolerance_temperature_for_step(self, value: 'float'):
        self.wrapped.AbsoluteToleranceTemperatureForStep = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_translational_velocity_for_newton_raphson(self) -> 'float':
        """float: 'AbsoluteToleranceTranslationalVelocityForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceTranslationalVelocityForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_translational_velocity_for_newton_raphson.setter
    def absolute_tolerance_translational_velocity_for_newton_raphson(self, value: 'float'):
        self.wrapped.AbsoluteToleranceTranslationalVelocityForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def absolute_tolerance_translational_velocity_for_step(self) -> 'float':
        """float: 'AbsoluteToleranceTranslationalVelocityForStep' is the original name of this property."""

        temp = self.wrapped.AbsoluteToleranceTranslationalVelocityForStep

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_translational_velocity_for_step.setter
    def absolute_tolerance_translational_velocity_for_step(self, value: 'float'):
        self.wrapped.AbsoluteToleranceTranslationalVelocityForStep = float(value) if value is not None else 0.0

    @property
    def damping_scaling_factor(self) -> 'float':
        """float: 'DampingScalingFactor' is the original name of this property."""

        temp = self.wrapped.DampingScalingFactor

        if temp is None:
            return 0.0

        return temp

    @damping_scaling_factor.setter
    def damping_scaling_factor(self, value: 'float'):
        self.wrapped.DampingScalingFactor = float(value) if value is not None else 0.0

    @property
    def damping_scaling_for_initial_transients(self) -> '_56.DampingScalingTypeForInitialTransients':
        """DampingScalingTypeForInitialTransients: 'DampingScalingForInitialTransients' is the original name of this property."""

        temp = self.wrapped.DampingScalingForInitialTransients

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_56.DampingScalingTypeForInitialTransients)(value) if value is not None else None

    @damping_scaling_for_initial_transients.setter
    def damping_scaling_for_initial_transients(self, value: '_56.DampingScalingTypeForInitialTransients'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DampingScalingForInitialTransients = value

    @property
    def end_time(self) -> 'float':
        """float: 'EndTime' is the original name of this property."""

        temp = self.wrapped.EndTime

        if temp is None:
            return 0.0

        return temp

    @end_time.setter
    def end_time(self, value: 'float'):
        self.wrapped.EndTime = float(value) if value is not None else 0.0

    @property
    def integration_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod':
        """enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod: 'IntegrationMethod' is the original name of this property."""

        temp = self.wrapped.IntegrationMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @integration_method.setter
    def integration_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_IntegrationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.IntegrationMethod = value

    @property
    def limit_time_step_for_final_results(self) -> 'bool':
        """bool: 'LimitTimeStepForFinalResults' is the original name of this property."""

        temp = self.wrapped.LimitTimeStepForFinalResults

        if temp is None:
            return False

        return temp

    @limit_time_step_for_final_results.setter
    def limit_time_step_for_final_results(self, value: 'bool'):
        self.wrapped.LimitTimeStepForFinalResults = bool(value) if value is not None else False

    @property
    def log_initial_transients(self) -> 'bool':
        """bool: 'LogInitialTransients' is the original name of this property."""

        temp = self.wrapped.LogInitialTransients

        if temp is None:
            return False

        return temp

    @log_initial_transients.setter
    def log_initial_transients(self, value: 'bool'):
        self.wrapped.LogInitialTransients = bool(value) if value is not None else False

    @property
    def maximum_number_of_time_steps(self) -> 'int':
        """int: 'MaximumNumberOfTimeSteps' is the original name of this property."""

        temp = self.wrapped.MaximumNumberOfTimeSteps

        if temp is None:
            return 0

        return temp

    @maximum_number_of_time_steps.setter
    def maximum_number_of_time_steps(self, value: 'int'):
        self.wrapped.MaximumNumberOfTimeSteps = int(value) if value is not None else 0

    @property
    def maximum_time_step(self) -> 'float':
        """float: 'MaximumTimeStep' is the original name of this property."""

        temp = self.wrapped.MaximumTimeStep

        if temp is None:
            return 0.0

        return temp

    @maximum_time_step.setter
    def maximum_time_step(self, value: 'float'):
        self.wrapped.MaximumTimeStep = float(value) if value is not None else 0.0

    @property
    def maximum_time_step_for_final_results(self) -> 'float':
        """float: 'MaximumTimeStepForFinalResults' is the original name of this property."""

        temp = self.wrapped.MaximumTimeStepForFinalResults

        if temp is None:
            return 0.0

        return temp

    @maximum_time_step_for_final_results.setter
    def maximum_time_step_for_final_results(self, value: 'float'):
        self.wrapped.MaximumTimeStepForFinalResults = float(value) if value is not None else 0.0

    @property
    def minimum_step_between_results(self) -> 'float':
        """float: 'MinimumStepBetweenResults' is the original name of this property."""

        temp = self.wrapped.MinimumStepBetweenResults

        if temp is None:
            return 0.0

        return temp

    @minimum_step_between_results.setter
    def minimum_step_between_results(self, value: 'float'):
        self.wrapped.MinimumStepBetweenResults = float(value) if value is not None else 0.0

    @property
    def minimum_time_step(self) -> 'float':
        """float: 'MinimumTimeStep' is the original name of this property."""

        temp = self.wrapped.MinimumTimeStep

        if temp is None:
            return 0.0

        return temp

    @minimum_time_step.setter
    def minimum_time_step(self, value: 'float'):
        self.wrapped.MinimumTimeStep = float(value) if value is not None else 0.0

    @property
    def rayleigh_damping_alpha(self) -> 'float':
        """float: 'RayleighDampingAlpha' is the original name of this property."""

        temp = self.wrapped.RayleighDampingAlpha

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_alpha.setter
    def rayleigh_damping_alpha(self, value: 'float'):
        self.wrapped.RayleighDampingAlpha = float(value) if value is not None else 0.0

    @property
    def rayleigh_damping_beta(self) -> 'float':
        """float: 'RayleighDampingBeta' is the original name of this property."""

        temp = self.wrapped.RayleighDampingBeta

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_beta.setter
    def rayleigh_damping_beta(self, value: 'float'):
        self.wrapped.RayleighDampingBeta = float(value) if value is not None else 0.0

    @property
    def relative_tolerance_simple(self) -> 'float':
        """float: 'RelativeToleranceSimple' is the original name of this property."""

        temp = self.wrapped.RelativeToleranceSimple

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance_simple.setter
    def relative_tolerance_simple(self, value: 'float'):
        self.wrapped.RelativeToleranceSimple = float(value) if value is not None else 0.0

    @property
    def relative_tolerance_for_newton_raphson(self) -> 'float':
        """float: 'RelativeToleranceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.RelativeToleranceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance_for_newton_raphson.setter
    def relative_tolerance_for_newton_raphson(self, value: 'float'):
        self.wrapped.RelativeToleranceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def relative_tolerance_for_step(self) -> 'float':
        """float: 'RelativeToleranceForStep' is the original name of this property."""

        temp = self.wrapped.RelativeToleranceForStep

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance_for_step.setter
    def relative_tolerance_for_step(self, value: 'float'):
        self.wrapped.RelativeToleranceForStep = float(value) if value is not None else 0.0

    @property
    def residual_force_tolerance_for_newton_raphson(self) -> 'float':
        """float: 'ResidualForceToleranceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.ResidualForceToleranceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @residual_force_tolerance_for_newton_raphson.setter
    def residual_force_tolerance_for_newton_raphson(self, value: 'float'):
        self.wrapped.ResidualForceToleranceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def residual_lagrange_angular_tolerance_for_newton_raphson(self) -> 'float':
        """float: 'ResidualLagrangeAngularToleranceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.ResidualLagrangeAngularToleranceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @residual_lagrange_angular_tolerance_for_newton_raphson.setter
    def residual_lagrange_angular_tolerance_for_newton_raphson(self, value: 'float'):
        self.wrapped.ResidualLagrangeAngularToleranceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def residual_lagrange_translational_tolerance_for_newton_raphson(self) -> 'float':
        """float: 'ResidualLagrangeTranslationalToleranceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.ResidualLagrangeTranslationalToleranceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @residual_lagrange_translational_tolerance_for_newton_raphson.setter
    def residual_lagrange_translational_tolerance_for_newton_raphson(self, value: 'float'):
        self.wrapped.ResidualLagrangeTranslationalToleranceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def residual_moment_tolerance_for_newton_raphson(self) -> 'float':
        """float: 'ResidualMomentToleranceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.ResidualMomentToleranceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @residual_moment_tolerance_for_newton_raphson.setter
    def residual_moment_tolerance_for_newton_raphson(self, value: 'float'):
        self.wrapped.ResidualMomentToleranceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def residual_relative_tolerance_for_newton_raphson(self) -> 'float':
        """float: 'ResidualRelativeToleranceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.ResidualRelativeToleranceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @residual_relative_tolerance_for_newton_raphson.setter
    def residual_relative_tolerance_for_newton_raphson(self, value: 'float'):
        self.wrapped.ResidualRelativeToleranceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def residual_temperature_tolerance_for_newton_raphson(self) -> 'float':
        """float: 'ResidualTemperatureToleranceForNewtonRaphson' is the original name of this property."""

        temp = self.wrapped.ResidualTemperatureToleranceForNewtonRaphson

        if temp is None:
            return 0.0

        return temp

    @residual_temperature_tolerance_for_newton_raphson.setter
    def residual_temperature_tolerance_for_newton_raphson(self, value: 'float'):
        self.wrapped.ResidualTemperatureToleranceForNewtonRaphson = float(value) if value is not None else 0.0

    @property
    def result_logging_frequency(self) -> '_82.ResultLoggingFrequency':
        """ResultLoggingFrequency: 'ResultLoggingFrequency' is the original name of this property."""

        temp = self.wrapped.ResultLoggingFrequency

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_82.ResultLoggingFrequency)(value) if value is not None else None

    @result_logging_frequency.setter
    def result_logging_frequency(self, value: '_82.ResultLoggingFrequency'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ResultLoggingFrequency = value

    @property
    def rotate_connections_with_bodies(self) -> 'bool':
        """bool: 'RotateConnectionsWithBodies' is the original name of this property."""

        temp = self.wrapped.RotateConnectionsWithBodies

        if temp is None:
            return False

        return temp

    @rotate_connections_with_bodies.setter
    def rotate_connections_with_bodies(self, value: 'bool'):
        self.wrapped.RotateConnectionsWithBodies = bool(value) if value is not None else False

    @property
    def solver_tolerance_input_method(self) -> '_89.TransientSolverToleranceInputMethod':
        """TransientSolverToleranceInputMethod: 'SolverToleranceInputMethod' is the original name of this property."""

        temp = self.wrapped.SolverToleranceInputMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_89.TransientSolverToleranceInputMethod)(value) if value is not None else None

    @solver_tolerance_input_method.setter
    def solver_tolerance_input_method(self, value: '_89.TransientSolverToleranceInputMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SolverToleranceInputMethod = value

    @property
    def theta(self) -> 'float':
        """float: 'Theta' is the original name of this property."""

        temp = self.wrapped.Theta

        if temp is None:
            return 0.0

        return temp

    @theta.setter
    def theta(self, value: 'float'):
        self.wrapped.Theta = float(value) if value is not None else 0.0

    @property
    def time_for_initial_transients(self) -> 'float':
        """float: 'TimeForInitialTransients' is the original name of this property."""

        temp = self.wrapped.TimeForInitialTransients

        if temp is None:
            return 0.0

        return temp

    @time_for_initial_transients.setter
    def time_for_initial_transients(self, value: 'float'):
        self.wrapped.TimeForInitialTransients = float(value) if value is not None else 0.0

    @property
    def time_step_length(self) -> 'float':
        """float: 'TimeStepLength' is the original name of this property."""

        temp = self.wrapped.TimeStepLength

        if temp is None:
            return 0.0

        return temp

    @time_step_length.setter
    def time_step_length(self, value: 'float'):
        self.wrapped.TimeStepLength = float(value) if value is not None else 0.0

    @property
    def time_to_start_using_final_results_maximum_time_step(self) -> 'float':
        """float: 'TimeToStartUsingFinalResultsMaximumTimeStep' is the original name of this property."""

        temp = self.wrapped.TimeToStartUsingFinalResultsMaximumTimeStep

        if temp is None:
            return 0.0

        return temp

    @time_to_start_using_final_results_maximum_time_step.setter
    def time_to_start_using_final_results_maximum_time_step(self, value: 'float'):
        self.wrapped.TimeToStartUsingFinalResultsMaximumTimeStep = float(value) if value is not None else 0.0

    @property
    def use_non_linear_solver_for_step(self) -> 'bool':
        """bool: 'UseNonLinearSolverForStep' is the original name of this property."""

        temp = self.wrapped.UseNonLinearSolverForStep

        if temp is None:
            return False

        return temp

    @use_non_linear_solver_for_step.setter
    def use_non_linear_solver_for_step(self, value: 'bool'):
        self.wrapped.UseNonLinearSolverForStep = bool(value) if value is not None else False
