﻿"""_6820.py

FlexiblePinAssemblyLoadCase
"""


from mastapy.utility import _1557
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.system_model.part_model import _2411
from mastapy.system_model.analyses_and_results.static_loads import _6884
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'FlexiblePinAssemblyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyLoadCase',)


class FlexiblePinAssemblyLoadCase(_6884.SpecialisedAssemblyLoadCase):
    """FlexiblePinAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(self) -> '_1557.LoadCaseOverrideOption':
        """LoadCaseOverrideOption: 'IncludeInnerRaceDistortionForFlexiblePinSpindle' is the original name of this property."""

        temp = self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1557.LoadCaseOverrideOption)(value) if value is not None else None

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    def include_inner_race_distortion_for_flexible_pin_spindle(self, value: '_1557.LoadCaseOverrideOption'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.IncludeInnerRaceDistortionForFlexiblePinSpindle = value

    @property
    def assembly_design(self) -> '_2411.FlexiblePinAssembly':
        """FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
