﻿"""_7294.py

PulleyAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2546, _2543
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6872, _6788
from mastapy.system_model.analyses_and_results.system_deflections import _2744
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7243
from mastapy._internal.python_net import python_net_import

_PULLEY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'PulleyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyAdvancedSystemDeflection',)


class PulleyAdvancedSystemDeflection(_7243.CouplingHalfAdvancedSystemDeflection):
    """PulleyAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _PULLEY_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'PulleyAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2546.Pulley':
        """Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2546.Pulley.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6872.PulleyLoadCase':
        """PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        if _6872.PulleyLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to PulleyLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_system_deflection_results(self) -> 'List[_2744.PulleySystemDeflection]':
        """List[PulleySystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
