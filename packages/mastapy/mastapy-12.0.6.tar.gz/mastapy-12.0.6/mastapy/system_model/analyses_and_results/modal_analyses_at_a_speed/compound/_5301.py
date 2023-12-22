﻿"""_5301.py

StraightBevelPlanetGearCompoundModalAnalysisAtASpeed
"""


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5172
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5295
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'StraightBevelPlanetGearCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearCompoundModalAnalysisAtASpeed',)


class StraightBevelPlanetGearCompoundModalAnalysisAtASpeed(_5295.StraightBevelDiffGearCompoundModalAnalysisAtASpeed):
    """StraightBevelPlanetGearCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases_ready(self) -> 'List[_5172.StraightBevelPlanetGearModalAnalysisAtASpeed]':
        """List[StraightBevelPlanetGearModalAnalysisAtASpeed]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5172.StraightBevelPlanetGearModalAnalysisAtASpeed]':
        """List[StraightBevelPlanetGearModalAnalysisAtASpeed]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
