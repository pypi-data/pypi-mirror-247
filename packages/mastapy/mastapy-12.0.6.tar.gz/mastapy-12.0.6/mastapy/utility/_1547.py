﻿"""_1547.py

DispatcherHelper
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DISPATCHER_HELPER = python_net_import('SMT.MastaAPI.Utility', 'DispatcherHelper')


__docformat__ = 'restructuredtext en'
__all__ = ('DispatcherHelper',)


class DispatcherHelper(_0.APIBase):
    """DispatcherHelper

    This is a mastapy class.
    """

    TYPE = _DISPATCHER_HELPER

    def __init__(self, instance_to_wrap: 'DispatcherHelper.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def disable_processing_count(self) -> 'int':
        """int: 'DisableProcessingCount' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DisableProcessingCount

        if temp is None:
            return 0

        return temp

    @property
    def frame_depth(self) -> 'int':
        """int: 'FrameDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrameDepth

        if temp is None:
            return 0

        return temp

    @property
    def has_shutdown_finished(self) -> 'bool':
        """bool: 'HasShutdownFinished' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasShutdownFinished

        if temp is None:
            return False

        return temp

    @property
    def has_shutdown_started(self) -> 'bool':
        """bool: 'HasShutdownStarted' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HasShutdownStarted

        if temp is None:
            return False

        return temp

    @property
    def is_suspended(self) -> 'bool':
        """bool: 'IsSuspended' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsSuspended

        if temp is None:
            return False

        return temp

    @property
    def number_of_queued_items(self) -> 'int':
        """int: 'NumberOfQueuedItems' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfQueuedItems

        if temp is None:
            return 0

        return temp

    @property
    def thread(self) -> 'str':
        """str: 'Thread' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Thread

        if temp is None:
            return ''

        return temp

    @property
    def timers(self) -> 'str':
        """str: 'Timers' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Timers

        if temp is None:
            return ''

        return temp

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
