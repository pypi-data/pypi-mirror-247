﻿"""_6471.py

ExcelBatchDutyCycleSpectraCreatorDetails
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles import _6472, _6475, _6474
from mastapy.utility import _1567
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_EXCEL_BATCH_DUTY_CYCLE_SPECTRA_CREATOR_DETAILS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles', 'ExcelBatchDutyCycleSpectraCreatorDetails')


__docformat__ = 'restructuredtext en'
__all__ = ('ExcelBatchDutyCycleSpectraCreatorDetails',)


class ExcelBatchDutyCycleSpectraCreatorDetails(_0.APIBase):
    """ExcelBatchDutyCycleSpectraCreatorDetails

    This is a mastapy class.
    """

    TYPE = _EXCEL_BATCH_DUTY_CYCLE_SPECTRA_CREATOR_DETAILS

    def __init__(self, instance_to_wrap: 'ExcelBatchDutyCycleSpectraCreatorDetails.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def excel_files_found(self) -> 'int':
        """int: 'ExcelFilesFound' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcelFilesFound

        if temp is None:
            return 0

        return temp

    @property
    def folder(self) -> 'str':
        """str: 'Folder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Folder

        if temp is None:
            return ''

        return temp

    @property
    def excel_file_details(self) -> '_6472.ExcelFileDetails':
        """ExcelFileDetails: 'ExcelFileDetails' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcelFileDetails

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def masta_file_details(self) -> '_6475.MASTAFileDetails':
        """MASTAFileDetails: 'MASTAFileDetails' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MASTAFileDetails

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def working_folder(self) -> '_1567.SelectableFolder':
        """SelectableFolder: 'WorkingFolder' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingFolder

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def excel_sheet_design_state_selection(self) -> 'List[_6474.ExcelSheetDesignStateSelector]':
        """List[ExcelSheetDesignStateSelector]: 'ExcelSheetDesignStateSelection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ExcelSheetDesignStateSelection

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

    def edit_folder_path(self):
        """ 'EditFolderPath' is the original name of this method."""

        self.wrapped.EditFolderPath()

    def prepare_working_folder(self):
        """ 'PrepareWorkingFolder' is the original name of this method."""

        self.wrapped.PrepareWorkingFolder()

    def write_masta_files(self):
        """ 'WriteMASTAFiles' is the original name of this method."""

        self.wrapped.WriteMASTAFiles()

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
