﻿"""_6852.py

KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
"""


from typing import List

from mastapy.system_model.part_model.gears import _2497
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6850, _6851, _6846
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase',)


class KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase(_6846.KlingelnbergCycloPalloidConicalGearSetLoadCase):
    """KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_LOAD_CASE

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase.TYPE'):
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
    def gears(self) -> 'List[_6850.KlingelnbergCycloPalloidSpiralBevelGearLoadCase]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearLoadCase]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_load_case(self) -> 'List[_6850.KlingelnbergCycloPalloidSpiralBevelGearLoadCase]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearLoadCase]: 'KlingelnbergCycloPalloidSpiralBevelGearsLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_load_case(self) -> 'List[_6851.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase]':
        """List[KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase]: 'KlingelnbergCycloPalloidSpiralBevelMeshesLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesLoadCase

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
