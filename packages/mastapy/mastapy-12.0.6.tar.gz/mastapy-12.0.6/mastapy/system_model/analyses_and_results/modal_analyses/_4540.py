﻿"""_4540.py

ClutchConnectionModalAnalysis
"""


from mastapy.system_model.connections_and_sockets.couplings import _2301
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6765
from mastapy.system_model.analyses_and_results.system_deflections import _2662
from mastapy.system_model.analyses_and_results.modal_analyses import _4557
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ClutchConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionModalAnalysis',)


class ClutchConnectionModalAnalysis(_4557.CouplingConnectionModalAnalysis):
    """ClutchConnectionModalAnalysis

    This is a mastapy class.
    """

    TYPE = _CLUTCH_CONNECTION_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'ClutchConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2301.ClutchConnection':
        """ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6765.ClutchConnectionLoadCase':
        """ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2662.ClutchConnectionSystemDeflection':
        """ClutchConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
