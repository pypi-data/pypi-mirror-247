﻿"""_4895.py

RollingRingConnectionModalAnalysisAtAStiffness
"""


from typing import List

from mastapy.system_model.connections_and_sockets import _2251
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6878
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4868
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'RollingRingConnectionModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionModalAnalysisAtAStiffness',)


class RollingRingConnectionModalAnalysisAtAStiffness(_4868.InterMountableComponentConnectionModalAnalysisAtAStiffness):
    """RollingRingConnectionModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _ROLLING_RING_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'RollingRingConnectionModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2251.RollingRingConnection':
        """RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6878.RollingRingConnectionLoadCase':
        """RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionModalAnalysisAtAStiffness]':
        """List[RollingRingConnectionModalAnalysisAtAStiffness]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
