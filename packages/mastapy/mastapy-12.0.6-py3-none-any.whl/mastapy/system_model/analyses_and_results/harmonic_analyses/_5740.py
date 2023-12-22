﻿"""_5740.py

RollingRingHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2552
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6879
from mastapy.system_model.analyses_and_results.system_deflections import _2750
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5660
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'RollingRingHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingHarmonicAnalysis',)


class RollingRingHarmonicAnalysis(_5660.CouplingHalfHarmonicAnalysis):
    """RollingRingHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'RollingRingHarmonicAnalysis.TYPE'):
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
    def component_load_case(self) -> '_6879.RollingRingLoadCase':
        """RollingRingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2750.RollingRingSystemDeflection':
        """RollingRingSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[RollingRingHarmonicAnalysis]':
        """List[RollingRingHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
