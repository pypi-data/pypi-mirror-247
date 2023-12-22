﻿"""_7346.py

BeltDriveCompoundAdvancedSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2532, _2542
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7213
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7434
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'BeltDriveCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundAdvancedSystemDeflection',)


class BeltDriveCompoundAdvancedSystemDeflection(_7434.SpecialisedAssemblyCompoundAdvancedSystemDeflection):
    """BeltDriveCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _BELT_DRIVE_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2532.BeltDrive':
        """BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        if _2532.BeltDrive.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltDrive. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2532.BeltDrive':
        """BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        if _2532.BeltDrive.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to BeltDrive. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_7213.BeltDriveAdvancedSystemDeflection]':
        """List[BeltDriveAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_7213.BeltDriveAdvancedSystemDeflection]':
        """List[BeltDriveAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
