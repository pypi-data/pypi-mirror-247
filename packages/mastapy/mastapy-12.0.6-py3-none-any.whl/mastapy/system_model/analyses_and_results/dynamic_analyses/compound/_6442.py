﻿"""_6442.py

SpiralBevelGearSetCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2500
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6313
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6440, _6441, _6359
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'SpiralBevelGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundDynamicAnalysis',)


class SpiralBevelGearSetCompoundDynamicAnalysis(_6359.BevelGearSetCompoundDynamicAnalysis):
    """SpiralBevelGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2500.SpiralBevelGearSet':
        """SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2500.SpiralBevelGearSet':
        """SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6313.SpiralBevelGearSetDynamicAnalysis]':
        """List[SpiralBevelGearSetDynamicAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_gears_compound_dynamic_analysis(self) -> 'List[_6440.SpiralBevelGearCompoundDynamicAnalysis]':
        """List[SpiralBevelGearCompoundDynamicAnalysis]: 'SpiralBevelGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelGearsCompoundDynamicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def spiral_bevel_meshes_compound_dynamic_analysis(self) -> 'List[_6441.SpiralBevelGearMeshCompoundDynamicAnalysis]':
        """List[SpiralBevelGearMeshCompoundDynamicAnalysis]: 'SpiralBevelMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpiralBevelMeshesCompoundDynamicAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6313.SpiralBevelGearSetDynamicAnalysis]':
        """List[SpiralBevelGearSetDynamicAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
