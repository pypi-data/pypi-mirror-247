﻿"""_4822.py

BoltModalAnalysisAtAStiffness
"""


from mastapy.system_model.part_model import _2399
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6764
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4827
from mastapy._internal.python_net import python_net_import

_BOLT_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'BoltModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltModalAnalysisAtAStiffness',)


class BoltModalAnalysisAtAStiffness(_4827.ComponentModalAnalysisAtAStiffness):
    """BoltModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _BOLT_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'BoltModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2399.Bolt':
        """Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6764.BoltLoadCase':
        """BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
