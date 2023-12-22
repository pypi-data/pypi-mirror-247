﻿"""_5228.py

CouplingConnectionCompoundModalAnalysisAtASpeed
"""


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5098
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5255
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'CouplingConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingConnectionCompoundModalAnalysisAtASpeed',)


class CouplingConnectionCompoundModalAnalysisAtASpeed(_5255.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed):
    """CouplingConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'CouplingConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_5098.CouplingConnectionModalAnalysisAtASpeed]':
        """List[CouplingConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_5098.CouplingConnectionModalAnalysisAtASpeed]':
        """List[CouplingConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
