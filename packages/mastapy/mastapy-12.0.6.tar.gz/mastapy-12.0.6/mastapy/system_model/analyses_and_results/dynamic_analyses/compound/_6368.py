﻿"""_6368.py

ConceptCouplingConnectionCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _2303
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6237
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6379
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'ConceptCouplingConnectionCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionCompoundDynamicAnalysis',)


class ConceptCouplingConnectionCompoundDynamicAnalysis(_6379.CouplingConnectionCompoundDynamicAnalysis):
    """ConceptCouplingConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2303.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2303.ConceptCouplingConnection':
        """ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_6237.ConceptCouplingConnectionDynamicAnalysis]':
        """List[ConceptCouplingConnectionDynamicAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_6237.ConceptCouplingConnectionDynamicAnalysis]':
        """List[ConceptCouplingConnectionDynamicAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
