﻿"""_5996.py

FaceGearHarmonicAnalysisOfSingleExcitation
"""


from mastapy.system_model.part_model.gears import _2484
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6816
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _6001
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'FaceGearHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearHarmonicAnalysisOfSingleExcitation',)


class FaceGearHarmonicAnalysisOfSingleExcitation(_6001.GearHarmonicAnalysisOfSingleExcitation):
    """FaceGearHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    def __init__(self, instance_to_wrap: 'FaceGearHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2484.FaceGear':
        """FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6816.FaceGearLoadCase':
        """FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
