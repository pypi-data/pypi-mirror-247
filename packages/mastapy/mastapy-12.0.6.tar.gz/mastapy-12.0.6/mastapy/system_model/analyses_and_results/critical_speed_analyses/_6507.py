﻿"""_6507.py

ConceptGearSetCriticalSpeedAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2478
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6775
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6505, _6506, _6538
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'ConceptGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetCriticalSpeedAnalysis',)


class ConceptGearSetCriticalSpeedAnalysis(_6538.GearSetCriticalSpeedAnalysis):
    """ConceptGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConceptGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2478.ConceptGearSet':
        """ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6775.ConceptGearSetLoadCase':
        """ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def concept_gears_critical_speed_analysis(self) -> 'List[_6505.ConceptGearCriticalSpeedAnalysis]':
        """List[ConceptGearCriticalSpeedAnalysis]: 'ConceptGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptGearsCriticalSpeedAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def concept_meshes_critical_speed_analysis(self) -> 'List[_6506.ConceptGearMeshCriticalSpeedAnalysis]':
        """List[ConceptGearMeshCriticalSpeedAnalysis]: 'ConceptMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConceptMeshesCriticalSpeedAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
