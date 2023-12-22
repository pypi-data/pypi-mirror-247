﻿"""_494.py

CylindricalGearSetRatingOptimisationHelper
"""


from typing import List

from mastapy.gears.rating.cylindrical.optimisation import (
    _495, _498, _500, _499,
    _496
)
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation', 'CylindricalGearSetRatingOptimisationHelper')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetRatingOptimisationHelper',)


class CylindricalGearSetRatingOptimisationHelper(_0.APIBase):
    """CylindricalGearSetRatingOptimisationHelper

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SET_RATING_OPTIMISATION_HELPER

    def __init__(self, instance_to_wrap: 'CylindricalGearSetRatingOptimisationHelper.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def helix_angle_optimisation_results(self) -> '_495.OptimisationResultsPair[_498.SafetyFactorOptimisationStepResultAngle]':
        """OptimisationResultsPair[SafetyFactorOptimisationStepResultAngle]: 'HelixAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleOptimisationResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_498.SafetyFactorOptimisationStepResultAngle](temp) if temp is not None else None

    @property
    def normal_module_optimisation_results(self) -> '_495.OptimisationResultsPair[_500.SafetyFactorOptimisationStepResultShortLength]':
        """OptimisationResultsPair[SafetyFactorOptimisationStepResultShortLength]: 'NormalModuleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalModuleOptimisationResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_500.SafetyFactorOptimisationStepResultShortLength](temp) if temp is not None else None

    @property
    def pressure_angle_optimisation_results(self) -> '_495.OptimisationResultsPair[_498.SafetyFactorOptimisationStepResultAngle]':
        """OptimisationResultsPair[SafetyFactorOptimisationStepResultAngle]: 'PressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PressureAngleOptimisationResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_498.SafetyFactorOptimisationStepResultAngle](temp) if temp is not None else None

    @property
    def profile_shift_coefficient_optimisation_results(self) -> '_495.OptimisationResultsPair[_499.SafetyFactorOptimisationStepResultNumber]':
        """OptimisationResultsPair[SafetyFactorOptimisationStepResultNumber]: 'ProfileShiftCoefficientOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ProfileShiftCoefficientOptimisationResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[_499.SafetyFactorOptimisationStepResultNumber](temp) if temp is not None else None

    @property
    def all_helix_angle_optimisation_results(self) -> 'List[_496.SafetyFactorOptimisationResults[_498.SafetyFactorOptimisationStepResultAngle]]':
        """List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'AllHelixAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllHelixAngleOptimisationResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def all_normal_module_optimisation_results(self) -> 'List[_496.SafetyFactorOptimisationResults[_500.SafetyFactorOptimisationStepResultShortLength]]':
        """List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultShortLength]]: 'AllNormalModuleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllNormalModuleOptimisationResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def all_normal_pressure_angle_optimisation_results(self) -> 'List[_496.SafetyFactorOptimisationResults[_498.SafetyFactorOptimisationStepResultAngle]]':
        """List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'AllNormalPressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllNormalPressureAngleOptimisationResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def all_profile_shift_optimisation_results(self) -> 'List[_496.SafetyFactorOptimisationResults[_499.SafetyFactorOptimisationStepResultNumber]]':
        """List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultNumber]]: 'AllProfileShiftOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllProfileShiftOptimisationResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def helix_angle_and_normal_pressure_angle_optimisation_results(self) -> 'List[_496.SafetyFactorOptimisationResults[_498.SafetyFactorOptimisationStepResultAngle]]':
        """List[SafetyFactorOptimisationResults[SafetyFactorOptimisationStepResultAngle]]: 'HelixAngleAndNormalPressureAngleOptimisationResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HelixAngleAndNormalPressureAngleOptimisationResults

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

    def calculate_optimisation_charts(self):
        """ 'CalculateOptimisationCharts' is the original name of this method."""

        self.wrapped.CalculateOptimisationCharts()

    def create_optimisation_report(self):
        """ 'CreateOptimisationReport' is the original name of this method."""

        self.wrapped.CreateOptimisationReport()

    def set_face_widths_for_required_safety_factor(self):
        """ 'SetFaceWidthsForRequiredSafetyFactor' is the original name of this method."""

        self.wrapped.SetFaceWidthsForRequiredSafetyFactor()

    def set_helix_angle_for_maximum_safety_factor(self):
        """ 'SetHelixAngleForMaximumSafetyFactor' is the original name of this method."""

        self.wrapped.SetHelixAngleForMaximumSafetyFactor()

    def set_normal_module_for_maximum_safety_factor(self):
        """ 'SetNormalModuleForMaximumSafetyFactor' is the original name of this method."""

        self.wrapped.SetNormalModuleForMaximumSafetyFactor()

    def set_pressure_angle_for_maximum_safety_factor(self):
        """ 'SetPressureAngleForMaximumSafetyFactor' is the original name of this method."""

        self.wrapped.SetPressureAngleForMaximumSafetyFactor()

    def set_profile_shift_coefficient_for_maximum_safety_factor(self):
        """ 'SetProfileShiftCoefficientForMaximumSafetyFactor' is the original name of this method."""

        self.wrapped.SetProfileShiftCoefficientForMaximumSafetyFactor()

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
