﻿"""_3377.py

DatumCompoundSteadyStateSynchronousResponseOnAShaft
"""


from typing import List

from mastapy.system_model.part_model import _2405
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3247
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import _3351
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound', 'DatumCompoundSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundSteadyStateSynchronousResponseOnAShaft',)


class DatumCompoundSteadyStateSynchronousResponseOnAShaft(_3351.ComponentCompoundSteadyStateSynchronousResponseOnAShaft):
    """DatumCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE = _DATUM_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    def __init__(self, instance_to_wrap: 'DatumCompoundSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2405.Datum':
        """Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3247.DatumSteadyStateSynchronousResponseOnAShaft]':
        """List[DatumSteadyStateSynchronousResponseOnAShaft]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3247.DatumSteadyStateSynchronousResponseOnAShaft]':
        """List[DatumSteadyStateSynchronousResponseOnAShaft]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
