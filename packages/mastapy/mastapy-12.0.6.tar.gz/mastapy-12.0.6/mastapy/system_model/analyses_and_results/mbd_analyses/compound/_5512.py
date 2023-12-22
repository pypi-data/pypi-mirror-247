﻿"""_5512.py

CVTCompoundMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy.system_model.analyses_and_results.mbd_analyses import _5363
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5481
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CVTCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundMultibodyDynamicsAnalysis',)


class CVTCompoundMultibodyDynamicsAnalysis(_5481.BeltDriveCompoundMultibodyDynamicsAnalysis):
    """CVTCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_5363.CVTMultibodyDynamicsAnalysis]':
        """List[CVTMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_5363.CVTMultibodyDynamicsAnalysis]':
        """List[CVTMultibodyDynamicsAnalysis]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
