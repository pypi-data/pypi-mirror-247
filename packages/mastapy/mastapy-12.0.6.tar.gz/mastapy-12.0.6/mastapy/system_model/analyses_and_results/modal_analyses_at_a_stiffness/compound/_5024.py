﻿"""_5024.py

RollingRingCompoundModalAnalysisAtAStiffness
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2552
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4896
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4971
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'RollingRingCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundModalAnalysisAtAStiffness',)


class RollingRingCompoundModalAnalysisAtAStiffness(_4971.CouplingHalfCompoundModalAnalysisAtAStiffness):
    """RollingRingCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'RollingRingCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2552.RollingRing':
        """RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4896.RollingRingModalAnalysisAtAStiffness]':
        """List[RollingRingModalAnalysisAtAStiffness]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundModalAnalysisAtAStiffness]':
        """List[RollingRingCompoundModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4896.RollingRingModalAnalysisAtAStiffness]':
        """List[RollingRingModalAnalysisAtAStiffness]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
