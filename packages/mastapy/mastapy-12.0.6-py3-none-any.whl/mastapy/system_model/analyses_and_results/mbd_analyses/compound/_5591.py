﻿"""_5591.py

TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2566
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5455
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5510
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis',)


class TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis(_5510.CouplingHalfCompoundMultibodyDynamicsAnalysis):
    """TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_TURBINE_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2566.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5455.TorqueConverterTurbineMultibodyDynamicsAnalysis]':
        """List[TorqueConverterTurbineMultibodyDynamicsAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5455.TorqueConverterTurbineMultibodyDynamicsAnalysis]':
        """List[TorqueConverterTurbineMultibodyDynamicsAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
