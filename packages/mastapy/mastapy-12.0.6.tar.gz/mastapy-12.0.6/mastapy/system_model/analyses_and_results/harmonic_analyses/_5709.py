﻿"""_5709.py

HypoidGearSetHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2491
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6839
from mastapy.system_model.analyses_and_results.system_deflections import _2715
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5707, _5708, _5627
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'HypoidGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetHarmonicAnalysis',)


class HypoidGearSetHarmonicAnalysis(_5627.AGMAGleasonConicalGearSetHarmonicAnalysis):
    """HypoidGearSetHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_SET_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'HypoidGearSetHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2491.HypoidGearSet':
        """HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6839.HypoidGearSetLoadCase':
        """HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2715.HypoidGearSetSystemDeflection':
        """HypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5707.HypoidGearHarmonicAnalysis]':
        """List[HypoidGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearsHarmonicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gears_harmonic_analysis(self) -> 'List[_5707.HypoidGearHarmonicAnalysis]':
        """List[HypoidGearHarmonicAnalysis]: 'HypoidGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearsHarmonicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5708.HypoidGearMeshHarmonicAnalysis]':
        """List[HypoidGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshesHarmonicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_meshes_harmonic_analysis(self) -> 'List[_5708.HypoidGearMeshHarmonicAnalysis]':
        """List[HypoidGearMeshHarmonicAnalysis]: 'HypoidMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidMeshesHarmonicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
