﻿"""_4432.py

CVTPulleyCompoundParametricStudyTool
"""


from typing import List

from mastapy.system_model.analyses_and_results.parametric_study_tools import _4285
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4478
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'CVTPulleyCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundParametricStudyTool',)


class CVTPulleyCompoundParametricStudyTool(_4478.PulleyCompoundParametricStudyTool):
    """CVTPulleyCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_COMPOUND_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_4285.CVTPulleyParametricStudyTool]':
        """List[CVTPulleyParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4285.CVTPulleyParametricStudyTool]':
        """List[CVTPulleyParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
