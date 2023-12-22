﻿"""_7383.py

CylindricalGearCompoundAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.gears import _2481, _2483
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.cylindrical import _449
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7251
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7394
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'CylindricalGearCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundAdvancedSystemDeflection',)


class CylindricalGearCompoundAdvancedSystemDeflection(_7394.GearCompoundAdvancedSystemDeflection):
    """CylindricalGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2481.CylindricalGear':
        """CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2481.CylindricalGear.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_duty_cycle_rating(self) -> '_449.CylindricalGearDutyCycleRating':
        """CylindricalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearDutyCycleRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_rating(self) -> '_449.CylindricalGearDutyCycleRating':
        """CylindricalGearDutyCycleRating: 'CylindricalGearRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_7251.CylindricalGearAdvancedSystemDeflection]':
        """List[CylindricalGearAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundAdvancedSystemDeflection]':
        """List[CylindricalGearCompoundAdvancedSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_7251.CylindricalGearAdvancedSystemDeflection]':
        """List[CylindricalGearAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
