﻿"""_3283.py

PowerLoadSteadyStateSynchronousResponseOnAShaft
"""


from mastapy.system_model.part_model import _2429
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6871
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3319
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'PowerLoadSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadSteadyStateSynchronousResponseOnAShaft',)


class PowerLoadSteadyStateSynchronousResponseOnAShaft(_3319.VirtualComponentSteadyStateSynchronousResponseOnAShaft):
    """PowerLoadSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    def __init__(self, instance_to_wrap: 'PowerLoadSteadyStateSynchronousResponseOnAShaft.TYPE'):
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
