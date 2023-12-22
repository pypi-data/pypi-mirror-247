﻿"""_678.py

ProcessSimulationInput
"""


from typing import List

from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _652, _656, _657, _683,
    _658
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.math_utility import _1501
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PROCESS_SIMULATION_INPUT = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'ProcessSimulationInput')


__docformat__ = 'restructuredtext en'
__all__ = ('ProcessSimulationInput',)


class ProcessSimulationInput(_0.APIBase):
    """ProcessSimulationInput

    This is a mastapy class.
    """

    TYPE = _PROCESS_SIMULATION_INPUT

    def __init__(self, instance_to_wrap: 'ProcessSimulationInput.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def analysis_setting(self) -> '_652.AnalysisMethod':
        """AnalysisMethod: 'AnalysisSetting' is the original name of this property."""

        temp = self.wrapped.AnalysisSetting

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_652.AnalysisMethod)(value) if value is not None else None

    @analysis_setting.setter
    def analysis_setting(self, value: '_652.AnalysisMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.AnalysisSetting = value

    @property
    def centre_distance_offset(self) -> 'float':
        """float: 'CentreDistanceOffset' is the original name of this property."""

        temp = self.wrapped.CentreDistanceOffset

        if temp is None:
            return 0.0

        return temp

    @centre_distance_offset.setter
    def centre_distance_offset(self, value: 'float'):
        self.wrapped.CentreDistanceOffset = float(value) if value is not None else 0.0

    @property
    def centre_distance_offset_specification_method(self) -> '_656.CentreDistanceOffsetMethod':
        """CentreDistanceOffsetMethod: 'CentreDistanceOffsetSpecificationMethod' is the original name of this property."""

        temp = self.wrapped.CentreDistanceOffsetSpecificationMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_656.CentreDistanceOffsetMethod)(value) if value is not None else None

    @centre_distance_offset_specification_method.setter
    def centre_distance_offset_specification_method(self, value: '_656.CentreDistanceOffsetMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CentreDistanceOffsetSpecificationMethod = value

    @property
    def feed(self) -> 'float':
        """float: 'Feed' is the original name of this property."""

        temp = self.wrapped.Feed

        if temp is None:
            return 0.0

        return temp

    @feed.setter
    def feed(self, value: 'float'):
        self.wrapped.Feed = float(value) if value is not None else 0.0

    @property
    def gear_design_lead_crown_modification(self) -> 'float':
        """float: 'GearDesignLeadCrownModification' is the original name of this property."""

        temp = self.wrapped.GearDesignLeadCrownModification

        if temp is None:
            return 0.0

        return temp

    @gear_design_lead_crown_modification.setter
    def gear_design_lead_crown_modification(self, value: 'float'):
        self.wrapped.GearDesignLeadCrownModification = float(value) if value is not None else 0.0

    @property
    def gear_designed_lead_crown_length(self) -> 'float':
        """float: 'GearDesignedLeadCrownLength' is the original name of this property."""

        temp = self.wrapped.GearDesignedLeadCrownLength

        if temp is None:
            return 0.0

        return temp

    @gear_designed_lead_crown_length.setter
    def gear_designed_lead_crown_length(self, value: 'float'):
        self.wrapped.GearDesignedLeadCrownLength = float(value) if value is not None else 0.0

    @property
    def shaft_angle_offset(self) -> 'float':
        """float: 'ShaftAngleOffset' is the original name of this property."""

        temp = self.wrapped.ShaftAngleOffset

        if temp is None:
            return 0.0

        return temp

    @shaft_angle_offset.setter
    def shaft_angle_offset(self, value: 'float'):
        self.wrapped.ShaftAngleOffset = float(value) if value is not None else 0.0

    @property
    def start_height_above_the_gear_center(self) -> 'float':
        """float: 'StartHeightAboveTheGearCenter' is the original name of this property."""

        temp = self.wrapped.StartHeightAboveTheGearCenter

        if temp is None:
            return 0.0

        return temp

    @start_height_above_the_gear_center.setter
    def start_height_above_the_gear_center(self, value: 'float'):
        self.wrapped.StartHeightAboveTheGearCenter = float(value) if value is not None else 0.0

    @property
    def tooth_index(self) -> 'int':
        """int: 'ToothIndex' is the original name of this property."""

        temp = self.wrapped.ToothIndex

        if temp is None:
            return 0

        return temp

    @tooth_index.setter
    def tooth_index(self, value: 'int'):
        self.wrapped.ToothIndex = int(value) if value is not None else 0

    @property
    def user_specified_center_distance_offset_relative_to_cutter_height(self) -> '_1501.Vector2DListAccessor':
        """Vector2DListAccessor: 'UserSpecifiedCenterDistanceOffsetRelativeToCutterHeight' is the original name of this property."""

        temp = self.wrapped.UserSpecifiedCenterDistanceOffsetRelativeToCutterHeight

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @user_specified_center_distance_offset_relative_to_cutter_height.setter
    def user_specified_center_distance_offset_relative_to_cutter_height(self, value: '_1501.Vector2DListAccessor'):
        self.wrapped.UserSpecifiedCenterDistanceOffsetRelativeToCutterHeight = value

    @property
    def cutter_head_slide_error(self) -> '_657.CutterHeadSlideError':
        """CutterHeadSlideError: 'CutterHeadSlideError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterHeadSlideError

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cutter_mounting_error(self) -> '_683.RackMountingError':
        """RackMountingError: 'CutterMountingError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CutterMountingError

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_mounting_error(self) -> '_658.GearMountingError':
        """GearMountingError: 'GearMountingError' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearMountingError

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
