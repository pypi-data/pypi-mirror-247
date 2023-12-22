﻿"""_3935.py

RingPinsCompoundStabilityAnalysis
"""


from typing import List

from mastapy.system_model.part_model.cycloidal import _2526
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3804
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3923
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'RingPinsCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundStabilityAnalysis',)


class RingPinsCompoundStabilityAnalysis(_3923.MountableComponentCompoundStabilityAnalysis):
    """RingPinsCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _RING_PINS_COMPOUND_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'RingPinsCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2526.RingPins':
        """RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3804.RingPinsStabilityAnalysis]':
        """List[RingPinsStabilityAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3804.RingPinsStabilityAnalysis]':
        """List[RingPinsStabilityAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
