﻿"""_3741.py

ConceptCouplingHalfStabilityAnalysis
"""


from mastapy.system_model.part_model.couplings import _2538
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6771
from mastapy.system_model.analyses_and_results.stability_analyses import _3752
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_HALF_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ConceptCouplingHalfStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingHalfStabilityAnalysis',)


class ConceptCouplingHalfStabilityAnalysis(_3752.CouplingHalfStabilityAnalysis):
    """ConceptCouplingHalfStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_HALF_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConceptCouplingHalfStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2538.ConceptCouplingHalf':
        """ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6771.ConceptCouplingHalfLoadCase':
        """ConceptCouplingHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
