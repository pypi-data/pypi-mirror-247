﻿"""_3528.py

KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed
"""


from typing import List

from mastapy.system_model.part_model.gears import _2497
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6852
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3529, _3527, _3522
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed',)


class KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed(_3522.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponseAtASpeed):
    """KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2497.KlingelnbergCycloPalloidSpiralBevelGearSet':
        """KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6852.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        """KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3529.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearsSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsSteadyStateSynchronousResponseAtASpeed

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3527.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelMeshesSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesSteadyStateSynchronousResponseAtASpeed

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
