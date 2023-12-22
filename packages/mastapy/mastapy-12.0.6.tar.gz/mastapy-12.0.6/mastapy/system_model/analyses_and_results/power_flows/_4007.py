﻿"""_4007.py

ConceptCouplingConnectionPowerFlow
"""


from mastapy.system_model.connections_and_sockets.couplings import _2303
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6770
from mastapy.system_model.analyses_and_results.power_flows import _4018
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConceptCouplingConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionPowerFlow',)


class ConceptCouplingConnectionPowerFlow(_4018.CouplingConnectionPowerFlow):
    """ConceptCouplingConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_CONNECTION_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def connection_load_case(self) -> '_6770.ConceptCouplingConnectionLoadCase':
        """ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
