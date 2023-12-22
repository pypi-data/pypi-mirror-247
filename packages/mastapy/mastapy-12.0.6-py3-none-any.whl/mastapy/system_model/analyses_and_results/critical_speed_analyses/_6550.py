﻿"""_6550.py

KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.gears import _2496
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6850
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6544
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis(_6544.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis):
    """KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2496.KlingelnbergCycloPalloidSpiralBevelGear':
        """KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6850.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        """KlingelnbergCycloPalloidSpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
