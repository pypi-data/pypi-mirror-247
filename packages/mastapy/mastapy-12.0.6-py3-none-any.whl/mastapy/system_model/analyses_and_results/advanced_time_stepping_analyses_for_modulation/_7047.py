﻿"""_7047.py

StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation
"""


from mastapy.system_model.part_model.gears import _2501, _2505, _2506
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6891, _6897, _6898
from mastapy.system_model.analyses_and_results.system_deflections import _2766, _2770, _2771
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6957
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation(_6957.BevelGearAdvancedTimeSteppingAnalysisForModulation):
    """StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2501.StraightBevelDiffGear':
        """StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2501.StraightBevelDiffGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6891.StraightBevelDiffGearLoadCase':
        """StraightBevelDiffGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        if _6891.StraightBevelDiffGearLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_load_case to StraightBevelDiffGearLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2766.StraightBevelDiffGearSystemDeflection':
        """StraightBevelDiffGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        if _2766.StraightBevelDiffGearSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to StraightBevelDiffGearSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
