﻿"""_3067.py

AbstractAssemblyCompoundSteadyStateSynchronousResponse
"""


from typing import List

from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _2934
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.compound import _3146
from mastapy._internal.python_net import python_net_import

_ABSTRACT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound', 'AbstractAssemblyCompoundSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractAssemblyCompoundSteadyStateSynchronousResponse',)


class AbstractAssemblyCompoundSteadyStateSynchronousResponse(_3146.PartCompoundSteadyStateSynchronousResponse):
    """AbstractAssemblyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    def __init__(self, instance_to_wrap: 'AbstractAssemblyCompoundSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self) -> 'List[_2934.AbstractAssemblySteadyStateSynchronousResponse]':
        """List[AbstractAssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2934.AbstractAssemblySteadyStateSynchronousResponse]':
        """List[AbstractAssemblySteadyStateSynchronousResponse]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
