﻿"""_2929.py

WormGearSetCompoundSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.gears import _2508
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _369
from mastapy.system_model.analyses_and_results.system_deflections import _2788
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2927, _2928, _2863
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'WormGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundSystemDeflection',)


class WormGearSetCompoundSystemDeflection(_2863.GearSetCompoundSystemDeflection):
    """WormGearSetCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2508.WormGearSet':
        """WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2508.WormGearSet':
        """WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def worm_gear_set_rating(self) -> '_369.WormGearSetDutyCycleRating':
        """WormGearSetDutyCycleRating: 'WormGearSetRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearSetRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2788.WormGearSetSystemDeflection]':
        """List[WormGearSetSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_gears_compound_system_deflection(self) -> 'List[_2927.WormGearCompoundSystemDeflection]':
        """List[WormGearCompoundSystemDeflection]: 'WormGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormGearsCompoundSystemDeflection

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def worm_meshes_compound_system_deflection(self) -> 'List[_2928.WormGearMeshCompoundSystemDeflection]':
        """List[WormGearMeshCompoundSystemDeflection]: 'WormMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WormMeshesCompoundSystemDeflection

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2788.WormGearSetSystemDeflection]':
        """List[WormGearSetSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
