﻿"""_6209.py

FlexiblePinAnalysisStopStartAnalysis
"""


from mastapy.system_model.analyses_and_results.system_deflections import _2755
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.flexible_pin_analyses import _6203
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ANALYSIS_STOP_START_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses', 'FlexiblePinAnalysisStopStartAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAnalysisStopStartAnalysis',)


class FlexiblePinAnalysisStopStartAnalysis(_6203.FlexiblePinAnalysis):
    """FlexiblePinAnalysisStopStartAnalysis

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ANALYSIS_STOP_START_ANALYSIS

    def __init__(self, instance_to_wrap: 'FlexiblePinAnalysisStopStartAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def shaft_extreme_load_case(self) -> '_2755.ShaftSystemDeflection':
        """ShaftSystemDeflection: 'ShaftExtremeLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftExtremeLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaft_nominal_load_case(self) -> '_2755.ShaftSystemDeflection':
        """ShaftSystemDeflection: 'ShaftNominalLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ShaftNominalLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
