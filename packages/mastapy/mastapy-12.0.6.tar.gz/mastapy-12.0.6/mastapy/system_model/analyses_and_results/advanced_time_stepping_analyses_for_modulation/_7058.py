﻿"""_7058.py

SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation
"""


from mastapy.system_model.part_model.couplings import _2562
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6902
from mastapy.system_model.analyses_and_results.system_deflections import _2774
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _7057
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation',)


class SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation(_7057.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation):
    """SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _SYNCHRONISER_SLEEVE_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2562.SynchroniserSleeve':
        """SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6902.SynchroniserSleeveLoadCase':
        """SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2774.SynchroniserSleeveSystemDeflection':
        """SynchroniserSleeveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
