﻿"""_3684.py

SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed
"""


from typing import List

from mastapy.system_model.part_model.gears import _2499
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3556
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3601
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed(_3601.BevelGearCompoundSteadyStateSynchronousResponseAtASpeed):
    """SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _SPIRAL_BEVEL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2499.SpiralBevelGear':
        """SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3556.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed]':
        """List[SpiralBevelGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3556.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed]':
        """List[SpiralBevelGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
