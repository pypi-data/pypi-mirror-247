﻿"""_5453.py

TorqueConverterPumpMultibodyDynamicsAnalysis
"""


from mastapy.system_model.part_model.couplings import _2564
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6906
from mastapy.system_model.analyses_and_results.mbd_analyses import _5360
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'TorqueConverterPumpMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpMultibodyDynamicsAnalysis',)


class TorqueConverterPumpMultibodyDynamicsAnalysis(_5360.CouplingHalfMultibodyDynamicsAnalysis):
    """TorqueConverterPumpMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_PUMP_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2564.TorqueConverterPump':
        """TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6906.TorqueConverterPumpLoadCase':
        """TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
