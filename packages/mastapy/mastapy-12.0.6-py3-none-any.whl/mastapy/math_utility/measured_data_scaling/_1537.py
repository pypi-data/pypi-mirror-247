﻿"""_1537.py

DataScalingOptions
"""


from typing import List

from mastapy._internal.implicit import enum_with_selected_value
from mastapy.math_utility import _1472, _1456
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy.math_utility.measured_data_scaling import _1538
from mastapy.utility.units_and_measurements.measurements import (
    _1580, _1585, _1589, _1604,
    _1610, _1662, _1661, _1667,
    _1583, _1700, _1693, _1638
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DATA_SCALING_OPTIONS = python_net_import('SMT.MastaAPI.MathUtility.MeasuredDataScaling', 'DataScalingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('DataScalingOptions',)


class DataScalingOptions(_0.APIBase):
    """DataScalingOptions

    This is a mastapy class.
    """

    TYPE = _DATA_SCALING_OPTIONS

    def __init__(self, instance_to_wrap: 'DataScalingOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def dynamic_scaling(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling':
        """enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling: 'DynamicScaling' is the original name of this property."""

        temp = self.wrapped.DynamicScaling

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @dynamic_scaling.setter
    def dynamic_scaling(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseScaling.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.DynamicScaling = value

    @property
    def weighting(self) -> '_1456.AcousticWeighting':
        """AcousticWeighting: 'Weighting' is the original name of this property."""

        temp = self.wrapped.Weighting

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1456.AcousticWeighting)(value) if value is not None else None

    @weighting.setter
    def weighting(self, value: '_1456.AcousticWeighting'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Weighting = value

    @property
    def acceleration_reference_values(self) -> '_1538.DataScalingReferenceValues[_1580.Acceleration]':
        """DataScalingReferenceValues[Acceleration]: 'AccelerationReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AccelerationReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1580.Acceleration](temp) if temp is not None else None

    @property
    def angular_acceleration_reference_values(self) -> '_1538.DataScalingReferenceValues[_1585.AngularAcceleration]':
        """DataScalingReferenceValues[AngularAcceleration]: 'AngularAccelerationReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularAccelerationReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1585.AngularAcceleration](temp) if temp is not None else None

    @property
    def angular_velocity_reference_values(self) -> '_1538.DataScalingReferenceValues[_1589.AngularVelocity]':
        """DataScalingReferenceValues[AngularVelocity]: 'AngularVelocityReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularVelocityReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1589.AngularVelocity](temp) if temp is not None else None

    @property
    def energy_reference_values(self) -> '_1538.DataScalingReferenceValues[_1604.Energy]':
        """DataScalingReferenceValues[Energy]: 'EnergyReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EnergyReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1604.Energy](temp) if temp is not None else None

    @property
    def force_reference_values(self) -> '_1538.DataScalingReferenceValues[_1610.Force]':
        """DataScalingReferenceValues[Force]: 'ForceReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ForceReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1610.Force](temp) if temp is not None else None

    @property
    def power_small_per_unit_area_reference_values(self) -> '_1538.DataScalingReferenceValues[_1662.PowerSmallPerArea]':
        """DataScalingReferenceValues[PowerSmallPerArea]: 'PowerSmallPerUnitAreaReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerSmallPerUnitAreaReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1662.PowerSmallPerArea](temp) if temp is not None else None

    @property
    def power_small_reference_values(self) -> '_1538.DataScalingReferenceValues[_1661.PowerSmall]':
        """DataScalingReferenceValues[PowerSmall]: 'PowerSmallReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerSmallReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1661.PowerSmall](temp) if temp is not None else None

    @property
    def pressure_reference_values(self) -> '_1538.DataScalingReferenceValues[_1667.Pressure]':
        """DataScalingReferenceValues[Pressure]: 'PressureReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1667.Pressure](temp) if temp is not None else None

    @property
    def small_angle_reference_values(self) -> '_1538.DataScalingReferenceValues[_1583.AngleSmall]':
        """DataScalingReferenceValues[AngleSmall]: 'SmallAngleReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SmallAngleReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1583.AngleSmall](temp) if temp is not None else None

    @property
    def small_velocity_reference_values(self) -> '_1538.DataScalingReferenceValues[_1700.VelocitySmall]':
        """DataScalingReferenceValues[VelocitySmall]: 'SmallVelocityReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SmallVelocityReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1700.VelocitySmall](temp) if temp is not None else None

    @property
    def torque_reference_values(self) -> '_1538.DataScalingReferenceValues[_1693.Torque]':
        """DataScalingReferenceValues[Torque]: 'TorqueReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorqueReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1693.Torque](temp) if temp is not None else None

    @property
    def very_short_length_reference_values(self) -> '_1538.DataScalingReferenceValues[_1638.LengthVeryShort]':
        """DataScalingReferenceValues[LengthVeryShort]: 'VeryShortLengthReferenceValues' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.VeryShortLengthReferenceValues

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_1638.LengthVeryShort](temp) if temp is not None else None

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
