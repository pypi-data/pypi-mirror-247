﻿"""_5118.py

FlexiblePinAssemblyModalAnalysisAtASpeed
"""


from mastapy.system_model.part_model import _2411
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6820
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5159
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'FlexiblePinAssemblyModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyModalAnalysisAtASpeed',)


class FlexiblePinAssemblyModalAnalysisAtASpeed(_5159.SpecialisedAssemblyModalAnalysisAtASpeed):
    """FlexiblePinAssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2411.FlexiblePinAssembly':
        """FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6820.FlexiblePinAssemblyLoadCase':
        """FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
