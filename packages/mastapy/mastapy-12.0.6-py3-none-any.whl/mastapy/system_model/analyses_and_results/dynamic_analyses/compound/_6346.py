﻿"""_6346.py

AGMAGleasonConicalGearMeshCompoundDynamicAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.dynamic_analyses import _6216
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6374
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'AGMAGleasonConicalGearMeshCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearMeshCompoundDynamicAnalysis',)


class AGMAGleasonConicalGearMeshCompoundDynamicAnalysis(_6374.ConicalGearMeshCompoundDynamicAnalysis):
    """AGMAGleasonConicalGearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearMeshCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_6216.AGMAGleasonConicalGearMeshDynamicAnalysis]':
        """List[AGMAGleasonConicalGearMeshDynamicAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_6216.AGMAGleasonConicalGearMeshDynamicAnalysis]':
        """List[AGMAGleasonConicalGearMeshDynamicAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
