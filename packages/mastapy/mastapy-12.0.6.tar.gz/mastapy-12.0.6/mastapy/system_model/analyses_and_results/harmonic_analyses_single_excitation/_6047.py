﻿"""_6047.py

SpringDamperHalfHarmonicAnalysisOfSingleExcitation
"""


from mastapy.system_model.part_model.couplings import _2557
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6889
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5981
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'SpringDamperHalfHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfHarmonicAnalysisOfSingleExcitation',)


class SpringDamperHalfHarmonicAnalysisOfSingleExcitation(_5981.CouplingHalfHarmonicAnalysisOfSingleExcitation):
    """SpringDamperHalfHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_HALF_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'SpringDamperHalfHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2557.SpringDamperHalf':
        """SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6889.SpringDamperHalfLoadCase':
        """SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
