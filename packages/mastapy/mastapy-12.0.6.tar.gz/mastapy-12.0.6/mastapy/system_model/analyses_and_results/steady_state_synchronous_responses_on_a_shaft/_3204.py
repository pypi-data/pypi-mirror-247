﻿"""_3204.py

BearingSteadyStateSynchronousResponseOnAShaft
"""


from typing import List

from mastapy.system_model.part_model import _2397
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6752
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3232
from mastapy._internal.python_net import python_net_import

_BEARING_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'BearingSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSteadyStateSynchronousResponseOnAShaft',)


class BearingSteadyStateSynchronousResponseOnAShaft(_3232.ConnectorSteadyStateSynchronousResponseOnAShaft):
    """BearingSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE = _BEARING_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    def __init__(self, instance_to_wrap: 'BearingSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2397.Bearing':
        """Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6752.BearingLoadCase':
        """BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[BearingSteadyStateSynchronousResponseOnAShaft]':
        """List[BearingSteadyStateSynchronousResponseOnAShaft]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
