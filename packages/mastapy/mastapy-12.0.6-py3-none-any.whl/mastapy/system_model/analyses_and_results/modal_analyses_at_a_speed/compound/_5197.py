﻿"""_5197.py

AssemblyCompoundModalAnalysisAtASpeed
"""


from typing import List

from mastapy.system_model.part_model import _2391, _2431
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5068
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5198, _5200, _5203, _5210,
    _5209, _5231, _5211, _5216,
    _5221, _5233, _5235, _5239,
    _5246, _5245, _5247, _5254,
    _5261, _5264, _5265, _5266,
    _5268, _5270, _5275, _5276,
    _5277, _5279, _5281, _5286,
    _5285, _5291, _5292, _5297,
    _5300, _5303, _5307, _5311,
    _5315, _5318, _5190
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'AssemblyCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysisAtASpeed',)


class AssemblyCompoundModalAnalysisAtASpeed(_5190.AbstractAssemblyCompoundModalAnalysisAtASpeed):
    """AssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2391.Assembly':
        """Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2391.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2391.Assembly':
        """Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2391.Assembly.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5068.AssemblyModalAnalysisAtASpeed]':
        """List[AssemblyModalAnalysisAtASpeed]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bearings(self) -> 'List[_5198.BearingCompoundModalAnalysisAtASpeed]':
        """List[BearingCompoundModalAnalysisAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bearings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def belt_drives(self) -> 'List[_5200.BeltDriveCompoundModalAnalysisAtASpeed]':
        """List[BeltDriveCompoundModalAnalysisAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BeltDrives

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5203.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed]':
        """List[BevelDifferentialGearSetCompoundModalAnalysisAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelDifferentialGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolted_joints(self) -> 'List[_5210.BoltedJointCompoundModalAnalysisAtASpeed]':
        """List[BoltedJointCompoundModalAnalysisAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BoltedJoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def bolts(self) -> 'List[_5209.BoltCompoundModalAnalysisAtASpeed]':
        """List[BoltCompoundModalAnalysisAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Bolts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cv_ts(self) -> 'List[_5231.CVTCompoundModalAnalysisAtASpeed]':
        """List[CVTCompoundModalAnalysisAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CVTs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def clutches(self) -> 'List[_5211.ClutchCompoundModalAnalysisAtASpeed]':
        """List[ClutchCompoundModalAnalysisAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Clutches

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_couplings(self) -> 'List[_5216.ConceptCouplingCompoundModalAnalysisAtASpeed]':
        """List[ConceptCouplingCompoundModalAnalysisAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5221.ConceptGearSetCompoundModalAnalysisAtASpeed]':
        """List[ConceptGearSetCompoundModalAnalysisAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5233.CycloidalAssemblyCompoundModalAnalysisAtASpeed]':
        """List[CycloidalAssemblyCompoundModalAnalysisAtASpeed]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5235.CycloidalDiscCompoundModalAnalysisAtASpeed]':
        """List[CycloidalDiscCompoundModalAnalysisAtASpeed]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CycloidalDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5239.CylindricalGearSetCompoundModalAnalysisAtASpeed]':
        """List[CylindricalGearSetCompoundModalAnalysisAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def fe_parts(self) -> 'List[_5246.FEPartCompoundModalAnalysisAtASpeed]':
        """List[FEPartCompoundModalAnalysisAtASpeed]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FEParts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def face_gear_sets(self) -> 'List[_5245.FaceGearSetCompoundModalAnalysisAtASpeed]':
        """List[FaceGearSetCompoundModalAnalysisAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5247.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed]':
        """List[FlexiblePinAssemblyCompoundModalAnalysisAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FlexiblePinAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5254.HypoidGearSetCompoundModalAnalysisAtASpeed]':
        """List[HypoidGearSetCompoundModalAnalysisAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5261.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed]':
        """List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidHypoidGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5264.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mass_discs(self) -> 'List[_5265.MassDiscCompoundModalAnalysisAtASpeed]':
        """List[MassDiscCompoundModalAnalysisAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MassDiscs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def measurement_components(self) -> 'List[_5266.MeasurementComponentCompoundModalAnalysisAtASpeed]':
        """List[MeasurementComponentCompoundModalAnalysisAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasurementComponents

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def oil_seals(self) -> 'List[_5268.OilSealCompoundModalAnalysisAtASpeed]':
        """List[OilSealCompoundModalAnalysisAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilSeals

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5270.PartToPartShearCouplingCompoundModalAnalysisAtASpeed]':
        """List[PartToPartShearCouplingCompoundModalAnalysisAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PartToPartShearCouplings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planet_carriers(self) -> 'List[_5275.PlanetCarrierCompoundModalAnalysisAtASpeed]':
        """List[PlanetCarrierCompoundModalAnalysisAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PlanetCarriers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def point_loads(self) -> 'List[_5276.PointLoadCompoundModalAnalysisAtASpeed]':
        """List[PointLoadCompoundModalAnalysisAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PointLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def power_loads(self) -> 'List[_5277.PowerLoadCompoundModalAnalysisAtASpeed]':
        """List[PowerLoadCompoundModalAnalysisAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoads

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def ring_pins(self) -> 'List[_5279.RingPinsCompoundModalAnalysisAtASpeed]':
        """List[RingPinsCompoundModalAnalysisAtASpeed]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPins

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5281.RollingRingAssemblyCompoundModalAnalysisAtASpeed]':
        """List[RollingRingAssemblyCompoundModalAnalysisAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollingRingAssemblies

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5286.ShaftHubConnectionCompoundModalAnalysisAtASpeed]':
        """List[ShaftHubConnectionCompoundModalAnalysisAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftHubConnections

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def shafts(self) -> 'List[_5285.ShaftCompoundModalAnalysisAtASpeed]':
        """List[ShaftCompoundModalAnalysisAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shafts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5291.SpiralBevelGearSetCompoundModalAnalysisAtASpeed]':
        """List[SpiralBevelGearSetCompoundModalAnalysisAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spring_dampers(self) -> 'List[_5292.SpringDamperCompoundModalAnalysisAtASpeed]':
        """List[SpringDamperCompoundModalAnalysisAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpringDampers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5297.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed]':
        """List[StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelDiffGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5300.StraightBevelGearSetCompoundModalAnalysisAtASpeed]':
        """List[StraightBevelGearSetCompoundModalAnalysisAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def synchronisers(self) -> 'List[_5303.SynchroniserCompoundModalAnalysisAtASpeed]':
        """List[SynchroniserCompoundModalAnalysisAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Synchronisers

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def torque_converters(self) -> 'List[_5307.TorqueConverterCompoundModalAnalysisAtASpeed]':
        """List[TorqueConverterCompoundModalAnalysisAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueConverters

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5311.UnbalancedMassCompoundModalAnalysisAtASpeed]':
        """List[UnbalancedMassCompoundModalAnalysisAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.UnbalancedMasses

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5315.WormGearSetCompoundModalAnalysisAtASpeed]':
        """List[WormGearSetCompoundModalAnalysisAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5318.ZerolBevelGearSetCompoundModalAnalysisAtASpeed]':
        """List[ZerolBevelGearSetCompoundModalAnalysisAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearSets

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5068.AssemblyModalAnalysisAtASpeed]':
        """List[AssemblyModalAnalysisAtASpeed]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
