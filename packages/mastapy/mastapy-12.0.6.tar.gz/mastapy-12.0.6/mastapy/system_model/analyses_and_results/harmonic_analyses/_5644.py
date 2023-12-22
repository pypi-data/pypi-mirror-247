﻿"""_5644.py

ClutchHarmonicAnalysis
"""


from mastapy.system_model.part_model.couplings import _2534
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6767
from mastapy.system_model.analyses_and_results.system_deflections import _2664
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5661
from mastapy._internal.python_net import python_net_import

_CLUTCH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ClutchHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHarmonicAnalysis',)


class ClutchHarmonicAnalysis(_5661.CouplingHarmonicAnalysis):
    """ClutchHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ClutchHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2534.Clutch':
        """Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6767.ClutchLoadCase':
        """ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2664.ClutchSystemDeflection':
        """ClutchSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
