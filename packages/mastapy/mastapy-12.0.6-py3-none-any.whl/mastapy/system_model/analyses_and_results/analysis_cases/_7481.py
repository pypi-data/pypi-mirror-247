﻿"""_7481.py

TimeSeriesLoadAnalysisCase
"""


from mastapy.system_model.analyses_and_results.static_loads import _6738
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _7465
from mastapy._internal.python_net import python_net_import

_TIME_SERIES_LOAD_ANALYSIS_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases', 'TimeSeriesLoadAnalysisCase')


__docformat__ = 'restructuredtext en'
__all__ = ('TimeSeriesLoadAnalysisCase',)


class TimeSeriesLoadAnalysisCase(_7465.AnalysisCase):
    """TimeSeriesLoadAnalysisCase

    This is a mastapy class.
    """

    TYPE = _TIME_SERIES_LOAD_ANALYSIS_CASE

    def __init__(self, instance_to_wrap: 'TimeSeriesLoadAnalysisCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_case(self) -> '_6738.TimeSeriesLoadCase':
        """TimeSeriesLoadCase: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
