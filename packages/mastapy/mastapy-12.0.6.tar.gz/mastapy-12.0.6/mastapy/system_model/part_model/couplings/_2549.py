﻿"""_2549.py

RigidConnectorToothLocation
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RIGID_CONNECTOR_TOOTH_LOCATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RigidConnectorToothLocation')


__docformat__ = 'restructuredtext en'
__all__ = ('RigidConnectorToothLocation',)


class RigidConnectorToothLocation(_0.APIBase):
    """RigidConnectorToothLocation

    This is a mastapy class.
    """

    TYPE = _RIGID_CONNECTOR_TOOTH_LOCATION

    def __init__(self, instance_to_wrap: 'RigidConnectorToothLocation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_angle(self) -> 'float':
        """float: 'CentreAngle' is the original name of this property."""

        temp = self.wrapped.CentreAngle

        if temp is None:
            return 0.0

        return temp

    @centre_angle.setter
    def centre_angle(self, value: 'float'):
        self.wrapped.CentreAngle = float(value) if value is not None else 0.0

    @property
    def end_angle(self) -> 'float':
        """float: 'EndAngle' is the original name of this property."""

        temp = self.wrapped.EndAngle

        if temp is None:
            return 0.0

        return temp

    @end_angle.setter
    def end_angle(self, value: 'float'):
        self.wrapped.EndAngle = float(value) if value is not None else 0.0

    @property
    def extent(self) -> 'float':
        """float: 'Extent' is the original name of this property."""

        temp = self.wrapped.Extent

        if temp is None:
            return 0.0

        return temp

    @extent.setter
    def extent(self, value: 'float'):
        self.wrapped.Extent = float(value) if value is not None else 0.0

    @property
    def id(self) -> 'int':
        """int: 'ID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ID

        if temp is None:
            return 0

        return temp

    @property
    def major_diameter_error(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'MajorDiameterError' is the original name of this property."""

        temp = self.wrapped.MajorDiameterError

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @major_diameter_error.setter
    def major_diameter_error(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.MajorDiameterError = value

    @property
    def major_diameter_radial_clearance(self) -> 'float':
        """float: 'MajorDiameterRadialClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MajorDiameterRadialClearance

        if temp is None:
            return 0.0

        return temp

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return ''

        return temp

    @property
    def normal_clearance_left_flank(self) -> 'float':
        """float: 'NormalClearanceLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalClearanceLeftFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_clearance_right_flank(self) -> 'float':
        """float: 'NormalClearanceRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalClearanceRightFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def pitch_error_left_flank(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PitchErrorLeftFlank' is the original name of this property."""

        temp = self.wrapped.PitchErrorLeftFlank

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @pitch_error_left_flank.setter
    def pitch_error_left_flank(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PitchErrorLeftFlank = value

    @property
    def pitch_error_right_flank(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'PitchErrorRightFlank' is the original name of this property."""

        temp = self.wrapped.PitchErrorRightFlank

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @pitch_error_right_flank.setter
    def pitch_error_right_flank(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.PitchErrorRightFlank = value

    @property
    def start_angle(self) -> 'float':
        """float: 'StartAngle' is the original name of this property."""

        temp = self.wrapped.StartAngle

        if temp is None:
            return 0.0

        return temp

    @start_angle.setter
    def start_angle(self, value: 'float'):
        self.wrapped.StartAngle = float(value) if value is not None else 0.0

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
