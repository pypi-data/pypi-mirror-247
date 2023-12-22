﻿"""_5969.py

ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation
"""


from mastapy.system_model.connections_and_sockets.couplings import _2303
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6770
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5980
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation',)


class ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation(_5980.CouplingConnectionHarmonicAnalysisOfSingleExcitation):
    """ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_CONNECTION_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2303.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6770.ConceptCouplingConnectionLoadCase':
        """ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
