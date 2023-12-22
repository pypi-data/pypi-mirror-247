﻿"""_5973.py

ConceptGearMeshHarmonicAnalysisOfSingleExcitation
"""


from mastapy.system_model.connections_and_sockets.gears import _2264
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6774
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _6002
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_MESH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'ConceptGearMeshHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearMeshHarmonicAnalysisOfSingleExcitation',)


class ConceptGearMeshHarmonicAnalysisOfSingleExcitation(_6002.GearMeshHarmonicAnalysisOfSingleExcitation):
    """ConceptGearMeshHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_MESH_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'ConceptGearMeshHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2264.ConceptGearMesh':
        """ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6774.ConceptGearMeshLoadCase':
        """ConceptGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
