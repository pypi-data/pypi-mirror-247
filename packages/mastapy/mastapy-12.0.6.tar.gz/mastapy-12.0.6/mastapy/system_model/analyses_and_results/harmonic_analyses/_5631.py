﻿"""_5631.py

BeltDriveHarmonicAnalysis
"""


from mastapy.system_model.part_model.couplings import _2532, _2542
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6754, _6787
from mastapy.system_model.analyses_and_results.system_deflections import _2651, _2685
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5746
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'BeltDriveHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveHarmonicAnalysis',)


class BeltDriveHarmonicAnalysis(_5746.SpecialisedAssemblyHarmonicAnalysis):
    """BeltDriveHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _BELT_DRIVE_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'BeltDriveHarmonicAnalysis.TYPE'):
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
    def system_deflection_results(self) -> '_2651.BeltDriveSystemDeflection':
        """BeltDriveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        if _2651.BeltDriveSystemDeflection.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast system_deflection_results to BeltDriveSystemDeflection. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
