﻿"""_5474.py

AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.mbd_analyses import _5322
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5506
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis',)


class AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis(_5506.ConnectionCompoundMultibodyDynamicsAnalysis):
    """AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(self) -> 'List[_5322.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]':
        """List[AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases_ready(self) -> 'List[_5322.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]':
        """List[AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
