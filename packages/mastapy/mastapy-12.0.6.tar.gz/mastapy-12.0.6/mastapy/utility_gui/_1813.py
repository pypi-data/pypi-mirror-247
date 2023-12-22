﻿"""_1813.py

DataInputFileOptions
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DATA_INPUT_FILE_OPTIONS = python_net_import('SMT.MastaAPI.UtilityGUI', 'DataInputFileOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('DataInputFileOptions',)


class DataInputFileOptions(_0.APIBase):
    """DataInputFileOptions

    This is a mastapy class.
    """

    TYPE = _DATA_INPUT_FILE_OPTIONS

    def __init__(self, instance_to_wrap: 'DataInputFileOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def column_headers_row(self) -> 'int':
        """int: 'ColumnHeadersRow' is the original name of this property."""

        temp = self.wrapped.ColumnHeadersRow

        if temp is None:
            return 0

        return temp

    @column_headers_row.setter
    def column_headers_row(self, value: 'int'):
        self.wrapped.ColumnHeadersRow = int(value) if value is not None else 0

    @property
    def data_end_row(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'DataEndRow' is the original name of this property."""

        temp = self.wrapped.DataEndRow

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @data_end_row.setter
    def data_end_row(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.DataEndRow = value

    @property
    def data_start_row(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'DataStartRow' is the original name of this property."""

        temp = self.wrapped.DataStartRow

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @data_start_row.setter
    def data_start_row(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.DataStartRow = value

    @property
    def selected_file_name(self) -> 'str':
        """str: 'SelectedFileName' is the original name of this property."""

        temp = self.wrapped.SelectedFileName

        if temp is None:
            return ''

        return temp

    @selected_file_name.setter
    def selected_file_name(self, value: 'str'):
        self.wrapped.SelectedFileName = str(value) if value is not None else ''

    @property
    def sheet(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'Sheet' is the original name of this property."""

        temp = self.wrapped.Sheet

        if temp is None:
            return ''

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else ''

    @sheet.setter
    def sheet(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.Sheet = value

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def open_file(self, filename: 'str'):
        """ 'OpenFile' is the original name of this method.

        Args:
            filename (str)
        """

        filename = str(filename)
        self.wrapped.OpenFile(filename if filename else '')

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
