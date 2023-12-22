﻿"""_6649.py

CVTPulleyCompoundCriticalSpeedAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6520
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6695
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CVTPulleyCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundCriticalSpeedAnalysis',)


class CVTPulleyCompoundCriticalSpeedAnalysis(_6695.PulleyCompoundCriticalSpeedAnalysis):
    """CVTPulleyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_6520.CVTPulleyCriticalSpeedAnalysis]':
        """List[CVTPulleyCriticalSpeedAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6520.CVTPulleyCriticalSpeedAnalysis]':
        """List[CVTPulleyCriticalSpeedAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
