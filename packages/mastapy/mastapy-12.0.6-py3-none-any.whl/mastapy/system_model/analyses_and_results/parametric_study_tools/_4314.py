﻿"""_4314.py

HypoidGearSetParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.gears import _2491
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6839
from mastapy.system_model.analyses_and_results.system_deflections import _2715
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4313, _4312, _4249
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'HypoidGearSetParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetParametricStudyTool',)


class HypoidGearSetParametricStudyTool(_4249.AGMAGleasonConicalGearSetParametricStudyTool):
    """HypoidGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_SET_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'HypoidGearSetParametricStudyTool.TYPE'):
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
    def assembly_system_deflection_results(self) -> 'List[_2715.HypoidGearSetSystemDeflection]':
        """List[HypoidGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblySystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gears_parametric_study_tool(self) -> 'List[_4313.HypoidGearParametricStudyTool]':
        """List[HypoidGearParametricStudyTool]: 'HypoidGearsParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearsParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_meshes_parametric_study_tool(self) -> 'List[_4312.HypoidGearMeshParametricStudyTool]':
        """List[HypoidGearMeshParametricStudyTool]: 'HypoidMeshesParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidMeshesParametricStudyTool

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
