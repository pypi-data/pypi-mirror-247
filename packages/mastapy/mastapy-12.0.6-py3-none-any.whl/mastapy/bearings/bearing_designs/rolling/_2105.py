﻿"""_2105.py

BearingProtection
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_designs.rolling import _2107
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_BEARING_PROTECTION = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'BearingProtection')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingProtection',)


class BearingProtection(_0.APIBase):
    """BearingProtection

    This is a mastapy class.
    """

    TYPE = _BEARING_PROTECTION

    def __init__(self, instance_to_wrap: 'BearingProtection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def advanced_bearing_results_hidden(self) -> 'str':
        """str: 'AdvancedBearingResultsHidden' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdvancedBearingResultsHidden

        if temp is None:
            return ''

        return temp

    @property
    def bearing_is_protected(self) -> 'bool':
        """bool: 'BearingIsProtected' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BearingIsProtected

        if temp is None:
            return False

        return temp

    @property
    def internal_geometry_hidden(self) -> 'str':
        """str: 'InternalGeometryHidden' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InternalGeometryHidden

        if temp is None:
            return ''

        return temp

    @property
    def protection_level(self) -> '_2107.BearingProtectionLevel':
        """BearingProtectionLevel: 'ProtectionLevel' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProtectionLevel

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2107.BearingProtectionLevel)(value) if value is not None else None

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
