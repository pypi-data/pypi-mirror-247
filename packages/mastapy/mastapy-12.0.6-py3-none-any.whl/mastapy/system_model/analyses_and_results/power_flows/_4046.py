﻿"""_4046.py

HypoidGearSetPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.gears import _2491
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6839
from mastapy.gears.rating.hypoid import _434
from mastapy.system_model.analyses_and_results.power_flows import _4045, _4044, _3987
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'HypoidGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetPowerFlow',)


class HypoidGearSetPowerFlow(_3987.AGMAGleasonConicalGearSetPowerFlow):
    """HypoidGearSetPowerFlow

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_SET_POWER_FLOW

    def __init__(self, instance_to_wrap: 'HypoidGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2491.HypoidGearSet':
        """HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6839.HypoidGearSetLoadCase':
        """HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating(self) -> '_434.HypoidGearSetRating':
        """HypoidGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Rating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_detailed_analysis(self) -> '_434.HypoidGearSetRating':
        """HypoidGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDetailedAnalysis

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears_power_flow(self) -> 'List[_4045.HypoidGearPowerFlow]':
        """List[HypoidGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearsPowerFlow

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_gears_power_flow(self) -> 'List[_4045.HypoidGearPowerFlow]':
        """List[HypoidGearPowerFlow]: 'HypoidGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidGearsPowerFlow

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def meshes_power_flow(self) -> 'List[_4044.HypoidGearMeshPowerFlow]':
        """List[HypoidGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshesPowerFlow

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def hypoid_meshes_power_flow(self) -> 'List[_4044.HypoidGearMeshPowerFlow]':
        """List[HypoidGearMeshPowerFlow]: 'HypoidMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HypoidMeshesPowerFlow

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
