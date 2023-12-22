﻿"""_6890.py

SpringDamperLoadCase
"""


from mastapy.system_model.part_model.couplings import _2556
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6785
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'SpringDamperLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperLoadCase',)


class SpringDamperLoadCase(_6785.CouplingLoadCase):
    """SpringDamperLoadCase

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_LOAD_CASE

    def __init__(self, instance_to_wrap: 'SpringDamperLoadCase.TYPE'):
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
