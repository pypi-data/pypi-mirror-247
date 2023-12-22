﻿"""_5280.py

RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed
"""


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _2300
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5151
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _5255
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed',)


class RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed(_5255.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed):
    """RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _RING_PINS_TO_DISC_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2300.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2300.RingPinsToDiscConnection':
        """RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_5151.RingPinsToDiscConnectionModalAnalysisAtASpeed]':
        """List[RingPinsToDiscConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_5151.RingPinsToDiscConnectionModalAnalysisAtASpeed]':
        """List[RingPinsToDiscConnectionModalAnalysisAtASpeed]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
