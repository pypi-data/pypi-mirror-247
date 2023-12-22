﻿"""_4565.py

CycloidalDiscModalAnalysis
"""


from mastapy.system_model.part_model.cycloidal import _2525
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6791
from mastapy.system_model.analyses_and_results.system_deflections import _2689
from mastapy.system_model.analyses_and_results.modal_analyses import _4520
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CycloidalDiscModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscModalAnalysis',)


class CycloidalDiscModalAnalysis(_4520.AbstractShaftModalAnalysis):
    """CycloidalDiscModalAnalysis

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'CycloidalDiscModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2525.CycloidalDisc':
        """CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6791.CycloidalDiscLoadCase':
        """CycloidalDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2689.CycloidalDiscSystemDeflection':
        """CycloidalDiscSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
