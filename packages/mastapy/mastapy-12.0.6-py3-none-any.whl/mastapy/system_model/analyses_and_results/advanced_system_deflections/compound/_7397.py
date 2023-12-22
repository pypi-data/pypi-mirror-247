﻿"""_7397.py

GuideDxfModelCompoundAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model import _2412
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7266
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7361
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'GuideDxfModelCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelCompoundAdvancedSystemDeflection',)


class GuideDxfModelCompoundAdvancedSystemDeflection(_7361.ComponentCompoundAdvancedSystemDeflection):
    """GuideDxfModelCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _GUIDE_DXF_MODEL_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'GuideDxfModelCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2412.GuideDxfModel':
        """GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_7266.GuideDxfModelAdvancedSystemDeflection]':
        """List[GuideDxfModelAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_7266.GuideDxfModelAdvancedSystemDeflection]':
        """List[GuideDxfModelAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
