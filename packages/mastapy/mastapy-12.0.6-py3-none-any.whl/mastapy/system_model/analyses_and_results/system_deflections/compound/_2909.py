﻿"""_2909.py

StraightBevelDiffGearCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.gears import _2501, _2505, _2506
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.system_deflections import _2766
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2818
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'StraightBevelDiffGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearCompoundSystemDeflection',)


class StraightBevelDiffGearCompoundSystemDeflection(_2818.BevelGearCompoundSystemDeflection):
    """StraightBevelDiffGearCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearCompoundSystemDeflection.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_2766.StraightBevelDiffGearSystemDeflection]':
        """List[StraightBevelDiffGearSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_2766.StraightBevelDiffGearSystemDeflection]':
        """List[StraightBevelDiffGearSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
