﻿"""_2651.py

BeltDriveSystemDeflection
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2532, _2542
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6754, _6787
from mastapy.system_model.analyses_and_results.power_flows import _3991, _4022
from mastapy.system_model.analyses_and_results.system_deflections import _2650, _2757
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BeltDriveSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveSystemDeflection',)


class BeltDriveSystemDeflection(_2757.SpecialisedAssemblySystemDeflection):
    """BeltDriveSystemDeflection

    This is a mastapy class.
    """

    TYPE = _BELT_DRIVE_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'BeltDriveSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def assembly_load_case(self) -> '_6754.BeltDriveLoadCase':
        """BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        if _6754.BeltDriveLoadCase.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to BeltDriveLoadCase. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_3991.BeltDrivePowerFlow':
        """BeltDrivePowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        if _3991.BeltDrivePowerFlow.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to BeltDrivePowerFlow. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def belts(self) -> 'List[_2650.BeltConnectionSystemDeflection]':
        """List[BeltConnectionSystemDeflection]: 'Belts' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Belts

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
