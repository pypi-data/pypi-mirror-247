﻿"""_4304.py

FaceGearParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.gears import _2484
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6816
from mastapy.system_model.analyses_and_results.system_deflections import _2707
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4309
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'FaceGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearParametricStudyTool',)


class FaceGearParametricStudyTool(_4309.GearParametricStudyTool):
    """FaceGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'FaceGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2484.FaceGear':
        """FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6816.FaceGearLoadCase':
        """FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2707.FaceGearSystemDeflection]':
        """List[FaceGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
