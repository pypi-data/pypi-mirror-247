﻿"""_1569.py

SystemDirectoryPopulator
"""


from typing import List

from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.utility import _1568
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SYSTEM_DIRECTORY_POPULATOR = python_net_import('SMT.MastaAPI.Utility', 'SystemDirectoryPopulator')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemDirectoryPopulator',)


class SystemDirectoryPopulator(_0.APIBase):
    """SystemDirectoryPopulator

    This is a mastapy class.
    """

    TYPE = _SYSTEM_DIRECTORY_POPULATOR

    def __init__(self, instance_to_wrap: 'SystemDirectoryPopulator.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def copy_from(self) -> 'SystemDirectoryPopulator.SetupFrom':
        """SetupFrom: 'CopyFrom' is the original name of this property."""

        temp = self.wrapped.CopyFrom

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(SystemDirectoryPopulator.SetupFrom)(value) if value is not None else None

    @copy_from.setter
    def copy_from(self, value: 'SystemDirectoryPopulator.SetupFrom'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CopyFrom = value

    @property
    def selected_version(self) -> 'list_with_selected_item.ListWithSelectedItem_SystemDirectory':
        """list_with_selected_item.ListWithSelectedItem_SystemDirectory: 'SelectedVersion' is the original name of this property."""

        temp = self.wrapped.SelectedVersion

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_SystemDirectory)(temp) if temp is not None else None

    @selected_version.setter
    def selected_version(self, value: 'list_with_selected_item.ListWithSelectedItem_SystemDirectory.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_SystemDirectory.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_SystemDirectory.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.SelectedVersion = value

    @property
    def current_version(self) -> '_1568.SystemDirectory':
        """SystemDirectory: 'CurrentVersion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentVersion

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def version_to_copy(self) -> '_1568.SystemDirectory':
        """SystemDirectory: 'VersionToCopy' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VersionToCopy

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

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
