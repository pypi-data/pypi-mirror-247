﻿"""_6505.py

ConceptGearCriticalSpeedAnalysis
"""


from mastapy.system_model.part_model.gears import _2477
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6773
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6536
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'ConceptGearCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCriticalSpeedAnalysis',)


class ConceptGearCriticalSpeedAnalysis(_6536.GearCriticalSpeedAnalysis):
    """ConceptGearCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_CRITICAL_SPEED_ANALYSIS

    def __init__(self, instance_to_wrap: 'ConceptGearCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2477.ConceptGear':
        """ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6773.ConceptGearLoadCase':
        """ConceptGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
