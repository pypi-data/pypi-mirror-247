﻿"""_2780.py

TorqueConverterPumpSystemDeflection
"""


from mastapy.system_model.part_model.couplings import _2564
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6906
from mastapy.system_model.analyses_and_results.power_flows import _4104
from mastapy.system_model.analyses_and_results.system_deflections import _2681
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'TorqueConverterPumpSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpSystemDeflection',)


class TorqueConverterPumpSystemDeflection(_2681.CouplingHalfSystemDeflection):
    """TorqueConverterPumpSystemDeflection

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_PUMP_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpSystemDeflection.TYPE'):
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

    @property
    def power_flow_results(self) -> '_4104.TorqueConverterPumpPowerFlow':
        """TorqueConverterPumpPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
