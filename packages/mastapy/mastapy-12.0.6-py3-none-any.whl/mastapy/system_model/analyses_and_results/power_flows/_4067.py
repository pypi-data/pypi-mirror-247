﻿"""_4067.py

PlanetCarrierPowerFlow
"""


from mastapy.system_model.part_model import _2426
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6867
from mastapy.system_model.analyses_and_results.power_flows import _4059
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PlanetCarrierPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierPowerFlow',)


class PlanetCarrierPowerFlow(_4059.MountableComponentPowerFlow):
    """PlanetCarrierPowerFlow

    This is a mastapy class.
    """

    TYPE = _PLANET_CARRIER_POWER_FLOW

    def __init__(self, instance_to_wrap: 'PlanetCarrierPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2426.PlanetCarrier':
        """PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6867.PlanetCarrierLoadCase':
        """PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
