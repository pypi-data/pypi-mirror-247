﻿"""_3802.py

PowerLoadStabilityAnalysis
"""


from mastapy.system_model.part_model import _2429
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6871
from mastapy.system_model.analyses_and_results.stability_analyses import _3839
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'PowerLoadStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadStabilityAnalysis',)


class PowerLoadStabilityAnalysis(_3839.VirtualComponentStabilityAnalysis):
    """PowerLoadStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'PowerLoadStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2429.PowerLoad':
        """PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6871.PowerLoadLoadCase':
        """PowerLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
