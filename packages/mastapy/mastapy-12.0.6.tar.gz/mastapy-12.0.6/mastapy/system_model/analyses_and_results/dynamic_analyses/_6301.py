﻿"""_6301.py

RingPinsDynamicAnalysis
"""


from mastapy.system_model.part_model.cycloidal import _2526
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6875
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6289
from mastapy._internal.python_net import python_net_import

_RING_PINS_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RingPinsDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsDynamicAnalysis',)


class RingPinsDynamicAnalysis(_6289.MountableComponentDynamicAnalysis):
    """RingPinsDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _RING_PINS_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'RingPinsDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2526.RingPins':
        """RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6875.RingPinsLoadCase':
        """RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
