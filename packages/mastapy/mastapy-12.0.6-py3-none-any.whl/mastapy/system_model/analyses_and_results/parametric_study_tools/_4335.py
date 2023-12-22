﻿"""_4335.py

ParametricStudyTool
"""


from mastapy.system_model.analyses_and_results.static_loads import _6737, _6744, _6738
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4334, _4336
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.analysis_cases import _7465
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyTool',)


class ParametricStudyTool(_7465.AnalysisCase):
    """ParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'ParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def load_case(self) -> '_6737.StaticLoadCase':
        """StaticLoadCase: 'LoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadCase

        if temp is None:
            return None

        if _6737.StaticLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast load_case to StaticLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def parametric_analysis_options(self) -> '_4336.ParametricStudyToolOptions':
        """ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ParametricAnalysisOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def time_series_load_case(self) -> '_6738.TimeSeriesLoadCase':
        """TimeSeriesLoadCase: 'TimeSeriesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TimeSeriesLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
