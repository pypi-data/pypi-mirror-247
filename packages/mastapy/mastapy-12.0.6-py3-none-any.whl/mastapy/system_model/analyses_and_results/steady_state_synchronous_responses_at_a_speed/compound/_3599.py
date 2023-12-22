﻿"""_3599.py

BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed
"""


from typing import List

from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3469
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3596
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed',)


class BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed(_3596.BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed):
    """BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_3469.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed]':
        """List[BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3469.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed]':
        """List[BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
