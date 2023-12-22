﻿"""_7340.py

AGMAGleasonConicalGearCompoundAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7207
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7368
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'AGMAGleasonConicalGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AGMAGleasonConicalGearCompoundAdvancedSystemDeflection',)


class AGMAGleasonConicalGearCompoundAdvancedSystemDeflection(_7368.ConicalGearCompoundAdvancedSystemDeflection):
    """AGMAGleasonConicalGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'AGMAGleasonConicalGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(self) -> 'List[_7207.AGMAGleasonConicalGearAdvancedSystemDeflection]':
        """List[AGMAGleasonConicalGearAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases_ready(self) -> 'List[_7207.AGMAGleasonConicalGearAdvancedSystemDeflection]':
        """List[AGMAGleasonConicalGearAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
