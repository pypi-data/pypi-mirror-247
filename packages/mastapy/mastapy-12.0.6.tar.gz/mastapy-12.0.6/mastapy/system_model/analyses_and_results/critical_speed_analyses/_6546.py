﻿"""_6546.py

KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.gears import _2493, _2495, _2497
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6510
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis',)


class KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis(_6510.ConicalGearSetCriticalSpeedAnalysis):
    """KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2493.KlingelnbergCycloPalloidConicalGearSet':
        """KlingelnbergCycloPalloidConicalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2493.KlingelnbergCycloPalloidConicalGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidConicalGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_2495.KlingelnbergCycloPalloidHypoidGearSet':
        """KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2495.KlingelnbergCycloPalloidHypoidGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_2497.KlingelnbergCycloPalloidSpiralBevelGearSet':
        """KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2497.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
