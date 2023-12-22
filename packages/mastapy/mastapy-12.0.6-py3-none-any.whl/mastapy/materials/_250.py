﻿"""_250.py

GeneralTransmissionProperties
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.materials import (
    _253, _285, _249, _281,
    _284, _237, _261, _283
)
from mastapy._internal.python_net import python_net_import
from mastapy import _0

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_GENERAL_TRANSMISSION_PROPERTIES = python_net_import('SMT.MastaAPI.Materials', 'GeneralTransmissionProperties')


__docformat__ = 'restructuredtext en'
__all__ = ('GeneralTransmissionProperties',)


class GeneralTransmissionProperties(_0.APIBase):
    """GeneralTransmissionProperties

    This is a mastapy class.
    """

    TYPE = _GENERAL_TRANSMISSION_PROPERTIES

    def __init__(self, instance_to_wrap: 'GeneralTransmissionProperties.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def agma_over_load_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'AGMAOverLoadFactor' is the original name of this property."""

        temp = self.wrapped.AGMAOverLoadFactor

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @agma_over_load_factor.setter
    def agma_over_load_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.AGMAOverLoadFactor = value

    @property
    def application_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'ApplicationFactor' is the original name of this property."""

        temp = self.wrapped.ApplicationFactor

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @application_factor.setter
    def application_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.ApplicationFactor = value

    @property
    def bearing_iso762006_static_safety_factor_limit(self) -> '_253.ISO76StaticSafetyFactorLimits':
        """ISO76StaticSafetyFactorLimits: 'BearingISO762006StaticSafetyFactorLimit' is the original name of this property."""

        temp = self.wrapped.BearingISO762006StaticSafetyFactorLimit

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_253.ISO76StaticSafetyFactorLimits)(value) if value is not None else None

    @bearing_iso762006_static_safety_factor_limit.setter
    def bearing_iso762006_static_safety_factor_limit(self, value: '_253.ISO76StaticSafetyFactorLimits'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BearingISO762006StaticSafetyFactorLimit = value

    @property
    def drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit(self) -> 'float':
        """float: 'DrawnCupNeedleRollerBearingsISO762006StaticSafetyFactorLimit' is the original name of this property."""

        temp = self.wrapped.DrawnCupNeedleRollerBearingsISO762006StaticSafetyFactorLimit

        if temp is None:
            return 0.0

        return temp

    @drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit.setter
    def drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit(self, value: 'float'):
        self.wrapped.DrawnCupNeedleRollerBearingsISO762006StaticSafetyFactorLimit = float(value) if value is not None else 0.0

    @property
    def driven_machine_characteristics(self) -> '_285.WorkingCharacteristics':
        """WorkingCharacteristics: 'DrivenMachineCharacteristics' is the original name of this property."""

        temp = self.wrapped.DrivenMachineCharacteristics

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_285.WorkingCharacteristics)(value) if value is not None else None

    @driven_machine_characteristics.setter
    def driven_machine_characteristics(self, value: '_285.WorkingCharacteristics'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DrivenMachineCharacteristics = value

    @property
    def driving_machine_characteristics(self) -> '_285.WorkingCharacteristics':
        """WorkingCharacteristics: 'DrivingMachineCharacteristics' is the original name of this property."""

        temp = self.wrapped.DrivingMachineCharacteristics

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_285.WorkingCharacteristics)(value) if value is not None else None

    @driving_machine_characteristics.setter
    def driving_machine_characteristics(self, value: '_285.WorkingCharacteristics'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DrivingMachineCharacteristics = value

    @property
    def energy_convergence_absolute_tolerance(self) -> 'float':
        """float: 'EnergyConvergenceAbsoluteTolerance' is the original name of this property."""

        temp = self.wrapped.EnergyConvergenceAbsoluteTolerance

        if temp is None:
            return 0.0

        return temp

    @energy_convergence_absolute_tolerance.setter
    def energy_convergence_absolute_tolerance(self, value: 'float'):
        self.wrapped.EnergyConvergenceAbsoluteTolerance = float(value) if value is not None else 0.0

    @property
    def feed_flow_rate(self) -> 'float':
        """float: 'FeedFlowRate' is the original name of this property."""

        temp = self.wrapped.FeedFlowRate

        if temp is None:
            return 0.0

        return temp

    @feed_flow_rate.setter
    def feed_flow_rate(self, value: 'float'):
        self.wrapped.FeedFlowRate = float(value) if value is not None else 0.0

    @property
    def feed_pressure(self) -> 'float':
        """float: 'FeedPressure' is the original name of this property."""

        temp = self.wrapped.FeedPressure

        if temp is None:
            return 0.0

        return temp

    @feed_pressure.setter
    def feed_pressure(self, value: 'float'):
        self.wrapped.FeedPressure = float(value) if value is not None else 0.0

    @property
    def gearing_type(self) -> '_249.GearingTypes':
        """GearingTypes: 'GearingType' is the original name of this property."""

        temp = self.wrapped.GearingType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_249.GearingTypes)(value) if value is not None else None

    @gearing_type.setter
    def gearing_type(self, value: '_249.GearingTypes'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearingType = value

    @property
    def iso2812007_safety_factor_requirement(self) -> 'float':
        """float: 'ISO2812007SafetyFactorRequirement' is the original name of this property."""

        temp = self.wrapped.ISO2812007SafetyFactorRequirement

        if temp is None:
            return 0.0

        return temp

    @iso2812007_safety_factor_requirement.setter
    def iso2812007_safety_factor_requirement(self, value: 'float'):
        self.wrapped.ISO2812007SafetyFactorRequirement = float(value) if value is not None else 0.0

    @property
    def isots162812008_safety_factor_requirement(self) -> 'float':
        """float: 'ISOTS162812008SafetyFactorRequirement' is the original name of this property."""

        temp = self.wrapped.ISOTS162812008SafetyFactorRequirement

        if temp is None:
            return 0.0

        return temp

    @isots162812008_safety_factor_requirement.setter
    def isots162812008_safety_factor_requirement(self, value: 'float'):
        self.wrapped.ISOTS162812008SafetyFactorRequirement = float(value) if value is not None else 0.0

    @property
    def include_ansiabma_ratings(self) -> 'bool':
        """bool: 'IncludeANSIABMARatings' is the original name of this property."""

        temp = self.wrapped.IncludeANSIABMARatings

        if temp is None:
            return False

        return temp

    @include_ansiabma_ratings.setter
    def include_ansiabma_ratings(self, value: 'bool'):
        self.wrapped.IncludeANSIABMARatings = bool(value) if value is not None else False

    @property
    def linear_bearings_minimum_axial_stiffness(self) -> 'float':
        """float: 'LinearBearingsMinimumAxialStiffness' is the original name of this property."""

        temp = self.wrapped.LinearBearingsMinimumAxialStiffness

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_axial_stiffness.setter
    def linear_bearings_minimum_axial_stiffness(self, value: 'float'):
        self.wrapped.LinearBearingsMinimumAxialStiffness = float(value) if value is not None else 0.0

    @property
    def linear_bearings_minimum_radial_stiffness(self) -> 'float':
        """float: 'LinearBearingsMinimumRadialStiffness' is the original name of this property."""

        temp = self.wrapped.LinearBearingsMinimumRadialStiffness

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_radial_stiffness.setter
    def linear_bearings_minimum_radial_stiffness(self, value: 'float'):
        self.wrapped.LinearBearingsMinimumRadialStiffness = float(value) if value is not None else 0.0

    @property
    def linear_bearings_minimum_tilt_stiffness(self) -> 'float':
        """float: 'LinearBearingsMinimumTiltStiffness' is the original name of this property."""

        temp = self.wrapped.LinearBearingsMinimumTiltStiffness

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_tilt_stiffness.setter
    def linear_bearings_minimum_tilt_stiffness(self, value: 'float'):
        self.wrapped.LinearBearingsMinimumTiltStiffness = float(value) if value is not None else 0.0

    @property
    def lubrication_detail_database(self) -> 'str':
        """str: 'LubricationDetailDatabase' is the original name of this property."""

        temp = self.wrapped.LubricationDetailDatabase.SelectedItemName

        if temp is None:
            return ''

        return temp

    @lubrication_detail_database.setter
    def lubrication_detail_database(self, value: 'str'):
        self.wrapped.LubricationDetailDatabase.SetSelectedItem(str(value) if value is not None else '')

    @property
    def mass(self) -> 'float':
        """float: 'Mass' is the original name of this property."""

        temp = self.wrapped.Mass

        if temp is None:
            return 0.0

        return temp

    @mass.setter
    def mass(self, value: 'float'):
        self.wrapped.Mass = float(value) if value is not None else 0.0

    @property
    def maximum_bearing_life_modification_factor(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MaximumBearingLifeModificationFactor' is the original name of this property."""

        temp = self.wrapped.MaximumBearingLifeModificationFactor

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @maximum_bearing_life_modification_factor.setter
    def maximum_bearing_life_modification_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MaximumBearingLifeModificationFactor = value

    @property
    def maximum_iso762006_static_safety_factor_for_a_loaded_bearing(self) -> 'float':
        """float: 'MaximumISO762006StaticSafetyFactorForALoadedBearing' is the original name of this property."""

        temp = self.wrapped.MaximumISO762006StaticSafetyFactorForALoadedBearing

        if temp is None:
            return 0.0

        return temp

    @maximum_iso762006_static_safety_factor_for_a_loaded_bearing.setter
    def maximum_iso762006_static_safety_factor_for_a_loaded_bearing(self, value: 'float'):
        self.wrapped.MaximumISO762006StaticSafetyFactorForALoadedBearing = float(value) if value is not None else 0.0

    @property
    def maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh(self) -> 'float':
        """float: 'MaximumStaticContactSafetyFactorForLoadedGearsInAMesh' is the original name of this property."""

        temp = self.wrapped.MaximumStaticContactSafetyFactorForLoadedGearsInAMesh

        if temp is None:
            return 0.0

        return temp

    @maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh.setter
    def maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh(self, value: 'float'):
        self.wrapped.MaximumStaticContactSafetyFactorForLoadedGearsInAMesh = float(value) if value is not None else 0.0

    @property
    def minimum_force_for_bearing_to_be_considered_loaded(self) -> 'float':
        """float: 'MinimumForceForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumForceForBearingToBeConsideredLoaded

        if temp is None:
            return 0.0

        return temp

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    def minimum_force_for_bearing_to_be_considered_loaded(self, value: 'float'):
        self.wrapped.MinimumForceForBearingToBeConsideredLoaded = float(value) if value is not None else 0.0

    @property
    def minimum_moment_for_bearing_to_be_considered_loaded(self) -> 'float':
        """float: 'MinimumMomentForBearingToBeConsideredLoaded' is the original name of this property."""

        temp = self.wrapped.MinimumMomentForBearingToBeConsideredLoaded

        if temp is None:
            return 0.0

        return temp

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    def minimum_moment_for_bearing_to_be_considered_loaded(self, value: 'float'):
        self.wrapped.MinimumMomentForBearingToBeConsideredLoaded = float(value) if value is not None else 0.0

    @property
    def minimum_static_safety_factor_for_maximum_contact_stress(self) -> 'float':
        """float: 'MinimumStaticSafetyFactorForMaximumContactStress' is the original name of this property."""

        temp = self.wrapped.MinimumStaticSafetyFactorForMaximumContactStress

        if temp is None:
            return 0.0

        return temp

    @minimum_static_safety_factor_for_maximum_contact_stress.setter
    def minimum_static_safety_factor_for_maximum_contact_stress(self, value: 'float'):
        self.wrapped.MinimumStaticSafetyFactorForMaximumContactStress = float(value) if value is not None else 0.0

    @property
    def non_linear_bearings_minimum_axial_stiffness(self) -> 'float':
        """float: 'NonLinearBearingsMinimumAxialStiffness' is the original name of this property."""

        temp = self.wrapped.NonLinearBearingsMinimumAxialStiffness

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_axial_stiffness.setter
    def non_linear_bearings_minimum_axial_stiffness(self, value: 'float'):
        self.wrapped.NonLinearBearingsMinimumAxialStiffness = float(value) if value is not None else 0.0

    @property
    def non_linear_bearings_minimum_radial_stiffness(self) -> 'float':
        """float: 'NonLinearBearingsMinimumRadialStiffness' is the original name of this property."""

        temp = self.wrapped.NonLinearBearingsMinimumRadialStiffness

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_radial_stiffness.setter
    def non_linear_bearings_minimum_radial_stiffness(self, value: 'float'):
        self.wrapped.NonLinearBearingsMinimumRadialStiffness = float(value) if value is not None else 0.0

    @property
    def non_linear_bearings_minimum_tilt_stiffness(self) -> 'float':
        """float: 'NonLinearBearingsMinimumTiltStiffness' is the original name of this property."""

        temp = self.wrapped.NonLinearBearingsMinimumTiltStiffness

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_tilt_stiffness.setter
    def non_linear_bearings_minimum_tilt_stiffness(self, value: 'float'):
        self.wrapped.NonLinearBearingsMinimumTiltStiffness = float(value) if value is not None else 0.0

    @property
    def permissible_track_truncation_ball_bearings(self) -> 'float':
        """float: 'PermissibleTrackTruncationBallBearings' is the original name of this property."""

        temp = self.wrapped.PermissibleTrackTruncationBallBearings

        if temp is None:
            return 0.0

        return temp

    @permissible_track_truncation_ball_bearings.setter
    def permissible_track_truncation_ball_bearings(self, value: 'float'):
        self.wrapped.PermissibleTrackTruncationBallBearings = float(value) if value is not None else 0.0

    @property
    def power_convergence_tolerance(self) -> 'float':
        """float: 'PowerConvergenceTolerance' is the original name of this property."""

        temp = self.wrapped.PowerConvergenceTolerance

        if temp is None:
            return 0.0

        return temp

    @power_convergence_tolerance.setter
    def power_convergence_tolerance(self, value: 'float'):
        self.wrapped.PowerConvergenceTolerance = float(value) if value is not None else 0.0

    @property
    def required_safety_factor_for_cvt_belt_clamping_force(self) -> 'float':
        """float: 'RequiredSafetyFactorForCVTBeltClampingForce' is the original name of this property."""

        temp = self.wrapped.RequiredSafetyFactorForCVTBeltClampingForce

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_cvt_belt_clamping_force.setter
    def required_safety_factor_for_cvt_belt_clamping_force(self, value: 'float'):
        self.wrapped.RequiredSafetyFactorForCVTBeltClampingForce = float(value) if value is not None else 0.0

    @property
    def safety_factor_against_plastic_strain(self) -> 'float':
        """float: 'SafetyFactorAgainstPlasticStrain' is the original name of this property."""

        temp = self.wrapped.SafetyFactorAgainstPlasticStrain

        if temp is None:
            return 0.0

        return temp

    @safety_factor_against_plastic_strain.setter
    def safety_factor_against_plastic_strain(self, value: 'float'):
        self.wrapped.SafetyFactorAgainstPlasticStrain = float(value) if value is not None else 0.0

    @property
    def safety_factor_against_sliding(self) -> 'float':
        """float: 'SafetyFactorAgainstSliding' is the original name of this property."""

        temp = self.wrapped.SafetyFactorAgainstSliding

        if temp is None:
            return 0.0

        return temp

    @safety_factor_against_sliding.setter
    def safety_factor_against_sliding(self, value: 'float'):
        self.wrapped.SafetyFactorAgainstSliding = float(value) if value is not None else 0.0

    @property
    def thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit(self) -> 'float':
        """float: 'ThrustSphericalRollerBearingsISO762006StaticSafetyFactorLimit' is the original name of this property."""

        temp = self.wrapped.ThrustSphericalRollerBearingsISO762006StaticSafetyFactorLimit

        if temp is None:
            return 0.0

        return temp

    @thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit.setter
    def thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit(self, value: 'float'):
        self.wrapped.ThrustSphericalRollerBearingsISO762006StaticSafetyFactorLimit = float(value) if value is not None else 0.0

    @property
    def transmission_application(self) -> '_281.TransmissionApplications':
        """TransmissionApplications: 'TransmissionApplication' is the original name of this property."""

        temp = self.wrapped.TransmissionApplication

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_281.TransmissionApplications)(value) if value is not None else None

    @transmission_application.setter
    def transmission_application(self, value: '_281.TransmissionApplications'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TransmissionApplication = value

    @property
    def volume(self) -> 'float':
        """float: 'Volume' is the original name of this property."""

        temp = self.wrapped.Volume

        if temp is None:
            return 0.0

        return temp

    @volume.setter
    def volume(self, value: 'float'):
        self.wrapped.Volume = float(value) if value is not None else 0.0

    @property
    def wind_turbine_standard(self) -> '_284.WindTurbineStandards':
        """WindTurbineStandards: 'WindTurbineStandard' is the original name of this property."""

        temp = self.wrapped.WindTurbineStandard

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_284.WindTurbineStandards)(value) if value is not None else None

    @wind_turbine_standard.setter
    def wind_turbine_standard(self, value: '_284.WindTurbineStandards'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WindTurbineStandard = value

    @property
    def zero_speed_tolerance(self) -> 'float':
        """float: 'ZeroSpeedTolerance' is the original name of this property."""

        temp = self.wrapped.ZeroSpeedTolerance

        if temp is None:
            return 0.0

        return temp

    @zero_speed_tolerance.setter
    def zero_speed_tolerance(self, value: 'float'):
        self.wrapped.ZeroSpeedTolerance = float(value) if value is not None else 0.0

    @property
    def air_properties(self) -> '_237.AirProperties':
        """AirProperties: 'AirProperties' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AirProperties

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def lubrication_detail(self) -> '_261.LubricationDetail':
        """LubricationDetail: 'LubricationDetail' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LubricationDetail

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def vehicle_dynamics(self) -> '_283.VehicleDynamicsProperties':
        """VehicleDynamicsProperties: 'VehicleDynamics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VehicleDynamics

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
