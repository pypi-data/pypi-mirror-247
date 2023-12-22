﻿"""_1550.py

FileHistory
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.utility import _1551
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_FILE_HISTORY = python_net_import('SMT.MastaAPI.Utility', 'FileHistory')


__docformat__ = 'restructuredtext en'
__all__ = ('FileHistory',)


class FileHistory(_0.APIBase):
    """FileHistory

    This is a mastapy class.
    """

    TYPE = _FILE_HISTORY

    def __init__(self, instance_to_wrap: 'FileHistory.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_history_items(self) -> 'int':
        """int: 'NumberOfHistoryItems' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfHistoryItems

        if temp is None:
            return 0

        return temp

    @property
    def items(self) -> 'List[_1551.FileHistoryItem]':
        """List[FileHistoryItem]: 'Items' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Items

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

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

    def clear_history(self):
        """ 'ClearHistory' is the original name of this method."""

        self.wrapped.ClearHistory()

    def add_file_history_item(self, item: '_1551.FileHistoryItem'):
        """ 'AddFileHistoryItem' is the original name of this method.

        Args:
            item (mastapy.utility.FileHistoryItem)
        """

        self.wrapped.AddFileHistoryItem(item.wrapped if item else None)

    def add_history_item(self, user_name: 'str', comment: 'str'):
        """ 'AddHistoryItem' is the original name of this method.

        Args:
            user_name (str)
            comment (str)
        """

        user_name = str(user_name)
        comment = str(comment)
        self.wrapped.AddHistoryItem(user_name if user_name else '', comment if comment else '')

    def create_history_item(self, user_name: 'str', comment: 'str') -> '_1551.FileHistoryItem':
        """ 'CreateHistoryItem' is the original name of this method.

        Args:
            user_name (str)
            comment (str)

        Returns:
            mastapy.utility.FileHistoryItem
        """

        user_name = str(user_name)
        comment = str(comment)
        method_result = self.wrapped.CreateHistoryItem(user_name if user_name else '', comment if comment else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

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
