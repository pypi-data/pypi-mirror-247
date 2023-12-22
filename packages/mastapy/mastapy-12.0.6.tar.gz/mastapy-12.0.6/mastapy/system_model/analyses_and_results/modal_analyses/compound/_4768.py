﻿"""_4768.py

ShaftCompoundModalAnalysis
"""


from typing import List

from mastapy.system_model.part_model.shaft_model import _2439
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4624
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4674
from mastapy._internal.python_net import python_net_import

_SHAFT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'ShaftCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftCompoundModalAnalysis',)


class ShaftCompoundModalAnalysis(_4674.AbstractShaftCompoundModalAnalysis):
    """ShaftCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE = _SHAFT_COMPOUND_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'ShaftCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2439.Shaft':
        """Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4624.ShaftModalAnalysis]':
        """List[ShaftModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[ShaftCompoundModalAnalysis]':
        """List[ShaftCompoundModalAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4624.ShaftModalAnalysis]':
        """List[ShaftModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
