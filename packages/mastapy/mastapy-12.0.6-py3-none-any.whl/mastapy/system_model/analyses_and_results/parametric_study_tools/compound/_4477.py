﻿"""_4477.py

PowerLoadCompoundParametricStudyTool
"""


from typing import List

from mastapy.system_model.part_model import _2429
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4348
from mastapy.system_model.analyses_and_results.static_loads import _6871
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4512
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PowerLoadCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundParametricStudyTool',)


class PowerLoadCompoundParametricStudyTool(_4512.VirtualComponentCompoundParametricStudyTool):
    """PowerLoadCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_COMPOUND_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2429.PowerLoad':
        """PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4348.PowerLoadParametricStudyTool]':
        """List[PowerLoadParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def load_cases(self) -> 'List[_6871.PowerLoadLoadCase]':
        """List[PowerLoadLoadCase]: 'LoadCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4348.PowerLoadParametricStudyTool]':
        """List[PowerLoadParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
