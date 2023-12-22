﻿"""_5083.py

ClutchHalfModalAnalysisAtASpeed
"""


from mastapy.system_model.part_model.couplings import _2535
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6766
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5099
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'ClutchHalfModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalfModalAnalysisAtASpeed',)


class ClutchHalfModalAnalysisAtASpeed(_5099.CouplingHalfModalAnalysisAtASpeed):
    """ClutchHalfModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HALF_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'ClutchHalfModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2535.ClutchHalf':
        """ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6766.ClutchHalfLoadCase':
        """ClutchHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
