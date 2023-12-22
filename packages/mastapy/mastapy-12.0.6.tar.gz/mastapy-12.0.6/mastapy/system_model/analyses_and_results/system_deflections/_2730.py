﻿"""_2730.py

MassDiscSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2419
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6853
from mastapy.system_model.analyses_and_results.power_flows import _4057
from mastapy.system_model.analyses_and_results.system_deflections import _2786
from mastapy._internal.python_net import python_net_import

_MASS_DISC_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'MassDiscSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('MassDiscSystemDeflection',)


class MassDiscSystemDeflection(_2786.VirtualComponentSystemDeflection):
    """MassDiscSystemDeflection

    This is a mastapy class.
    """

    TYPE = _MASS_DISC_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'MassDiscSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2419.MassDisc':
        """MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6853.MassDiscLoadCase':
        """MassDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_4057.MassDiscPowerFlow':
        """MassDiscPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def planetaries(self) -> 'List[MassDiscSystemDeflection]':
        """List[MassDiscSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
