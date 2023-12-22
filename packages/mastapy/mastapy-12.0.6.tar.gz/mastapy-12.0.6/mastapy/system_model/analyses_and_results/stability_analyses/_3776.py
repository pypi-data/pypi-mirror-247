﻿"""_3776.py

GuideDxfModelStabilityAnalysis
"""


from mastapy.system_model.part_model import _2412
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6828
from mastapy.system_model.analyses_and_results.stability_analyses import _3739
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'GuideDxfModelStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelStabilityAnalysis',)


class GuideDxfModelStabilityAnalysis(_3739.ComponentStabilityAnalysis):
    """GuideDxfModelStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _GUIDE_DXF_MODEL_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'GuideDxfModelStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2412.GuideDxfModel':
        """GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6828.GuideDxfModelLoadCase':
        """GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
