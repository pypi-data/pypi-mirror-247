﻿"""_4388.py

ZerolBevelGearParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model.gears import _2509
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6917
from mastapy.system_model.analyses_and_results.system_deflections import _2792
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4260
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ZerolBevelGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearParametricStudyTool',)


class ZerolBevelGearParametricStudyTool(_4260.BevelGearParametricStudyTool):
    """ZerolBevelGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'ZerolBevelGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2509.ZerolBevelGear':
        """ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6917.ZerolBevelGearLoadCase':
        """ZerolBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2792.ZerolBevelGearSystemDeflection]':
        """List[ZerolBevelGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
