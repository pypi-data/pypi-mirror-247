﻿"""_6834.py

HarmonicLoadDataImportFromMotorPackages
"""


from typing import Generic, TypeVar

from mastapy._internal.implicit import list_with_selected_item, enum_with_selected_value
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.electric_machines.harmonic_load_data import _1350
from mastapy.system_model.analyses_and_results.static_loads import _6833, _6812
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_IMPORT_FROM_MOTOR_PACKAGES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataImportFromMotorPackages')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataImportFromMotorPackages',)


T = TypeVar('T', bound='_6812.ElectricMachineHarmonicLoadImportOptionsBase')


class HarmonicLoadDataImportFromMotorPackages(_6833.HarmonicLoadDataImportBase['T'], Generic[T]):
    """HarmonicLoadDataImportFromMotorPackages

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _HARMONIC_LOAD_DATA_IMPORT_FROM_MOTOR_PACKAGES

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataImportFromMotorPackages.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_slice_number(self) -> 'list_with_selected_item.ListWithSelectedItem_int':
        """list_with_selected_item.ListWithSelectedItem_int: 'AxialSliceNumber' is the original name of this property."""

        temp = self.wrapped.AxialSliceNumber

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_int)(temp) if temp is not None else 0

    @axial_slice_number.setter
    def axial_slice_number(self, value: 'list_with_selected_item.ListWithSelectedItem_int.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_int.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0)
        self.wrapped.AxialSliceNumber = value

    @property
    def data_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType':
        """enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType: 'DataType' is the original name of this property."""

        temp = self.wrapped.DataType

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @data_type.setter
    def data_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DataType = value

    @property
    def speed(self) -> 'list_with_selected_item.ListWithSelectedItem_float':
        """list_with_selected_item.ListWithSelectedItem_float: 'Speed' is the original name of this property."""

        temp = self.wrapped.Speed

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_float)(temp) if temp is not None else 0.0

    @speed.setter
    def speed(self, value: 'list_with_selected_item.ListWithSelectedItem_float.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_float.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0)
        self.wrapped.Speed = value
