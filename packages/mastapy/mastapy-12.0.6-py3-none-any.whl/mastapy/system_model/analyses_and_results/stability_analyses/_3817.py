﻿"""_3817.py

SpringDamperConnectionStabilityAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2309
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6888
from mastapy.system_model.analyses_and_results.stability_analyses import _3751
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SpringDamperConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperConnectionStabilityAnalysis',)


class SpringDamperConnectionStabilityAnalysis(_3751.CouplingConnectionStabilityAnalysis):
    """SpringDamperConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_CONNECTION_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpringDamperConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2309.SpringDamperConnection':
        """SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6888.SpringDamperConnectionLoadCase':
        """SpringDamperConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
