﻿"""_7365.py

ConceptGearCompoundAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.gears import _2477
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7232
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7394
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'ConceptGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundAdvancedSystemDeflection',)


class ConceptGearCompoundAdvancedSystemDeflection(_7394.GearCompoundAdvancedSystemDeflection):
    """ConceptGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONCEPT_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundAdvancedSystemDeflection.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_7232.ConceptGearAdvancedSystemDeflection]':
        """List[ConceptGearAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_7232.ConceptGearAdvancedSystemDeflection]':
        """List[ConceptGearAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
