﻿"""_50.py

AnalysisSettingsItem
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _80, _81
from mastapy.utility.databases import _1795
from mastapy._internal.python_net import python_net_import

_ANALYSIS_SETTINGS_ITEM = python_net_import('SMT.MastaAPI.NodalAnalysis', 'AnalysisSettingsItem')


__docformat__ = 'restructuredtext en'
__all__ = ('AnalysisSettingsItem',)


class AnalysisSettingsItem(_1795.NamedDatabaseItem):
    """AnalysisSettingsItem

    This is a mastapy class.
    """

    TYPE = _ANALYSIS_SETTINGS_ITEM

    def __init__(self, instance_to_wrap: 'AnalysisSettingsItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        """float: 'GearMeshNodesPerUnitLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio

        if temp is None:
            return 0.0

        return temp

    @gear_mesh_nodes_per_unit_length_to_diameter_ratio.setter
    def gear_mesh_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.GearMeshNodesPerUnitLengthToDiameterRatio = float(value) if value is not None else 0.0

    @property
    def maximum_section_length_to_diameter_ratio(self) -> 'float':
        """float: 'MaximumSectionLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.MaximumSectionLengthToDiameterRatio

        if temp is None:
            return 0.0

        return temp

    @maximum_section_length_to_diameter_ratio.setter
    def maximum_section_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.MaximumSectionLengthToDiameterRatio = float(value) if value is not None else 0.0

    @property
    def minimum_number_of_gear_mesh_nodes(self) -> 'int':
        """int: 'MinimumNumberOfGearMeshNodes' is the original name of this property."""

        temp = self.wrapped.MinimumNumberOfGearMeshNodes

        if temp is None:
            return 0

        return temp

    @minimum_number_of_gear_mesh_nodes.setter
    def minimum_number_of_gear_mesh_nodes(self, value: 'int'):
        self.wrapped.MinimumNumberOfGearMeshNodes = int(value) if value is not None else 0

    @property
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(self) -> 'bool':
        """bool: 'OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations' is the original name of this property."""

        temp = self.wrapped.OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations

        if temp is None:
            return False

        return temp

    @overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations.setter
    def overwrite_advanced_system_deflection_load_cases_created_for_harmonic_excitations(self, value: 'bool'):
        self.wrapped.OverwriteAdvancedSystemDeflectionLoadCasesCreatedForHarmonicExcitations = bool(value) if value is not None else False

    @property
    def rating_type_for_bearing_reliability(self) -> '_80.RatingTypeForBearingReliability':
        """RatingTypeForBearingReliability: 'RatingTypeForBearingReliability' is the original name of this property."""

        temp = self.wrapped.RatingTypeForBearingReliability

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_80.RatingTypeForBearingReliability)(value) if value is not None else None

    @rating_type_for_bearing_reliability.setter
    def rating_type_for_bearing_reliability(self, value: '_80.RatingTypeForBearingReliability'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RatingTypeForBearingReliability = value

    @property
    def rating_type_for_shaft_reliability(self) -> '_81.RatingTypeForShaftReliability':
        """RatingTypeForShaftReliability: 'RatingTypeForShaftReliability' is the original name of this property."""

        temp = self.wrapped.RatingTypeForShaftReliability

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_81.RatingTypeForShaftReliability)(value) if value is not None else None

    @rating_type_for_shaft_reliability.setter
    def rating_type_for_shaft_reliability(self, value: '_81.RatingTypeForShaftReliability'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RatingTypeForShaftReliability = value

    @property
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(self) -> 'bool':
        """bool: 'RemoveRigidBodyRotationThetaZTwistFromShaftReporting' is the original name of this property."""

        temp = self.wrapped.RemoveRigidBodyRotationThetaZTwistFromShaftReporting

        if temp is None:
            return False

        return temp

    @remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting.setter
    def remove_rigid_body_rotation_theta_z_twist_from_shaft_reporting(self, value: 'bool'):
        self.wrapped.RemoveRigidBodyRotationThetaZTwistFromShaftReporting = bool(value) if value is not None else False

    @property
    def spline_nodes_per_unit_length_to_diameter_ratio(self) -> 'float':
        """float: 'SplineNodesPerUnitLengthToDiameterRatio' is the original name of this property."""

        temp = self.wrapped.SplineNodesPerUnitLengthToDiameterRatio

        if temp is None:
            return 0.0

        return temp

    @spline_nodes_per_unit_length_to_diameter_ratio.setter
    def spline_nodes_per_unit_length_to_diameter_ratio(self, value: 'float'):
        self.wrapped.SplineNodesPerUnitLengthToDiameterRatio = float(value) if value is not None else 0.0

    @property
    def system_deflection_maximum_iterations(self) -> 'int':
        """int: 'SystemDeflectionMaximumIterations' is the original name of this property."""

        temp = self.wrapped.SystemDeflectionMaximumIterations

        if temp is None:
            return 0

        return temp

    @system_deflection_maximum_iterations.setter
    def system_deflection_maximum_iterations(self, value: 'int'):
        self.wrapped.SystemDeflectionMaximumIterations = int(value) if value is not None else 0

    @property
    def use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability(self) -> 'bool':
        """bool: 'UseMeanLoadAndLoadSharingFactorForPlanetBearingReliability' is the original name of this property."""

        temp = self.wrapped.UseMeanLoadAndLoadSharingFactorForPlanetBearingReliability

        if temp is None:
            return False

        return temp

    @use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability.setter
    def use_mean_load_and_load_sharing_factor_for_planet_bearing_reliability(self, value: 'bool'):
        self.wrapped.UseMeanLoadAndLoadSharingFactorForPlanetBearingReliability = bool(value) if value is not None else False

    @property
    def use_single_node_for_cylindrical_gear_meshes(self) -> 'bool':
        """bool: 'UseSingleNodeForCylindricalGearMeshes' is the original name of this property."""

        temp = self.wrapped.UseSingleNodeForCylindricalGearMeshes

        if temp is None:
            return False

        return temp

    @use_single_node_for_cylindrical_gear_meshes.setter
    def use_single_node_for_cylindrical_gear_meshes(self, value: 'bool'):
        self.wrapped.UseSingleNodeForCylindricalGearMeshes = bool(value) if value is not None else False

    @property
    def use_single_node_for_spline_connections(self) -> 'bool':
        """bool: 'UseSingleNodeForSplineConnections' is the original name of this property."""

        temp = self.wrapped.UseSingleNodeForSplineConnections

        if temp is None:
            return False

        return temp

    @use_single_node_for_spline_connections.setter
    def use_single_node_for_spline_connections(self, value: 'bool'):
        self.wrapped.UseSingleNodeForSplineConnections = bool(value) if value is not None else False
