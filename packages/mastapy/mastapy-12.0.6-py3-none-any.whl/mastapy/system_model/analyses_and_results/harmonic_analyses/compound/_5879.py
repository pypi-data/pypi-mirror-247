﻿"""_5879.py

InterMountableComponentConnectionCompoundHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5710
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5849
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'InterMountableComponentConnectionCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('InterMountableComponentConnectionCompoundHarmonicAnalysis',)


class InterMountableComponentConnectionCompoundHarmonicAnalysis(_5849.ConnectionCompoundHarmonicAnalysis):
    """InterMountableComponentConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'InterMountableComponentConnectionCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_5710.InterMountableComponentConnectionHarmonicAnalysis]':
        """List[InterMountableComponentConnectionHarmonicAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_5710.InterMountableComponentConnectionHarmonicAnalysis]':
        """List[InterMountableComponentConnectionHarmonicAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
