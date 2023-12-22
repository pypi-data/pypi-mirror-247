﻿"""_3819.py

SpringDamperStabilityAnalysis
"""


from mastapy.system_model.part_model.couplings import _2556
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6890
from mastapy.system_model.analyses_and_results.stability_analyses import _3753
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SpringDamperStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperStabilityAnalysis',)


class SpringDamperStabilityAnalysis(_3753.CouplingStabilityAnalysis):
    """SpringDamperStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'SpringDamperStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2556.SpringDamper':
        """SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6890.SpringDamperLoadCase':
        """SpringDamperLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
