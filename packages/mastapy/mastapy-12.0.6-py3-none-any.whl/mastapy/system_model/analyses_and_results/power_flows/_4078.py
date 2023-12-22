﻿"""_4078.py

RootAssemblyPowerFlow
"""


from mastapy.system_model.part_model import _2431
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4069, _3988
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'RootAssemblyPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyPowerFlow',)


class RootAssemblyPowerFlow(_3988.AssemblyPowerFlow):
    """RootAssemblyPowerFlow

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_POWER_FLOW

    def __init__(self, instance_to_wrap: 'RootAssemblyPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2431.RootAssembly':
        """RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_inputs(self) -> '_4069.PowerFlow':
        """PowerFlow: 'PowerFlowInputs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
