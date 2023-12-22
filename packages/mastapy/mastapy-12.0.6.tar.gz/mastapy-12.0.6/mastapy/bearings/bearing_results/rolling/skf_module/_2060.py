﻿"""_2060.py

SKFCredentials
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.bearings.bearing_results.rolling.skf_module import _2058
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SKF_CREDENTIALS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'SKFCredentials')


__docformat__ = 'restructuredtext en'
__all__ = ('SKFCredentials',)


class SKFCredentials(_0.APIBase):
    """SKFCredentials

    This is a mastapy class.
    """

    TYPE = _SKF_CREDENTIALS

    def __init__(self, instance_to_wrap: 'SKFCredentials.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def email_address(self) -> 'str':
        """str: 'EmailAddress' is the original name of this property."""

        temp = self.wrapped.EmailAddress

        if temp is None:
            return ''

        return temp

    @email_address.setter
    def email_address(self, value: 'str'):
        self.wrapped.EmailAddress = str(value) if value is not None else ''

    @property
    def password(self) -> 'str':
        """str: 'Password' is the original name of this property."""

        temp = self.wrapped.Password

        if temp is None:
            return ''

        return temp

    @password.setter
    def password(self, value: 'str'):
        self.wrapped.Password = str(value) if value is not None else ''

    @property
    def read_accept_terms_of_use(self) -> 'bool':
        """bool: 'ReadAcceptTermsOfUse' is the original name of this property."""

        temp = self.wrapped.ReadAcceptTermsOfUse

        if temp is None:
            return False

        return temp

    @read_accept_terms_of_use.setter
    def read_accept_terms_of_use(self, value: 'bool'):
        self.wrapped.ReadAcceptTermsOfUse = bool(value) if value is not None else False

    @property
    def skf_authentication(self) -> '_2058.SKFAuthentication':
        """SKFAuthentication: 'SKFAuthentication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SKFAuthentication

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

    def authenticate(self):
        """ 'Authenticate' is the original name of this method."""

        self.wrapped.Authenticate()

    def create_skf_account(self):
        """ 'CreateSKFAccount' is the original name of this method."""

        self.wrapped.CreateSKFAccount()

    def skf_privacy_notice(self):
        """ 'SKFPrivacyNotice' is the original name of this method."""

        self.wrapped.SKFPrivacyNotice()

    def skf_terms_of_use(self):
        """ 'SKFTermsOfUse' is the original name of this method."""

        self.wrapped.SKFTermsOfUse()

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
