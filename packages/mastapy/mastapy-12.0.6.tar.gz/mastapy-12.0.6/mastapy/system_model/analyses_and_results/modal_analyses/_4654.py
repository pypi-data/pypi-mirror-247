﻿"""_4654.py

WhineWaterfallSettings
"""


from typing import List

from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4572, _4556, _4573, _4604,
    _4653, _4606, _4652
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.math_utility import (
    _1461, _1500, _1486, _1493
)
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.harmonic_analyses.results import (
    _5779, _5787, _5782, _5788
)
from mastapy.math_utility.measured_data_scaling import _1537
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5692, _5704, _5747
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _7003
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.drawing.options import _2222, _2220
from mastapy.utility.property import _1808
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_WHINE_WATERFALL_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'WhineWaterfallSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('WhineWaterfallSettings',)


class WhineWaterfallSettings(_0.APIBase):
    """WhineWaterfallSettings

    This is a mastapy class.
    """

    TYPE = _WHINE_WATERFALL_SETTINGS

    def __init__(self, instance_to_wrap: 'WhineWaterfallSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def chart_type(self) -> '_4572.DynamicsResponse3DChartType':
        """DynamicsResponse3DChartType: 'ChartType' is the original name of this property."""

        temp = self.wrapped.ChartType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_4572.DynamicsResponse3DChartType)(value) if value is not None else None

    @chart_type.setter
    def chart_type(self, value: '_4572.DynamicsResponse3DChartType'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ChartType = value

    @property
    def complex_component(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption':
        """enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption: 'ComplexComponent' is the original name of this property."""

        temp = self.wrapped.ComplexComponent

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @complex_component.setter
    def complex_component(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ComplexComponent = value

    @property
    def connected_component_type(self) -> '_5779.ConnectedComponentType':
        """ConnectedComponentType: 'ConnectedComponentType' is the original name of this property."""

        temp = self.wrapped.ConnectedComponentType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_5779.ConnectedComponentType)(value) if value is not None else None

    @connected_component_type.setter
    def connected_component_type(self, value: '_5779.ConnectedComponentType'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ConnectedComponentType = value

    @property
    def coordinate_system(self) -> '_4556.CoordinateSystemForWhine':
        """CoordinateSystemForWhine: 'CoordinateSystem' is the original name of this property."""

        temp = self.wrapped.CoordinateSystem

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_4556.CoordinateSystemForWhine)(value) if value is not None else None

    @coordinate_system.setter
    def coordinate_system(self, value: '_4556.CoordinateSystemForWhine'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CoordinateSystem = value

    @property
    def max_harmonic(self) -> 'overridable.Overridable_int':
        """overridable.Overridable_int: 'MaxHarmonic' is the original name of this property."""

        temp = self.wrapped.MaxHarmonic

        if temp is None:
            return 0

        return constructor.new_from_mastapy_type(overridable.Overridable_int)(temp) if temp is not None else 0

    @max_harmonic.setter
    def max_harmonic(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0, is_overridden)
        self.wrapped.MaxHarmonic = value

    @property
    def maximum_order(self) -> 'float':
        """float: 'MaximumOrder' is the original name of this property."""

        temp = self.wrapped.MaximumOrder

        if temp is None:
            return 0.0

        return temp

    @maximum_order.setter
    def maximum_order(self, value: 'float'):
        self.wrapped.MaximumOrder = float(value) if value is not None else 0.0

    @property
    def minimum_order(self) -> 'float':
        """float: 'MinimumOrder' is the original name of this property."""

        temp = self.wrapped.MinimumOrder

        if temp is None:
            return 0.0

        return temp

    @minimum_order.setter
    def minimum_order(self, value: 'float'):
        self.wrapped.MinimumOrder = float(value) if value is not None else 0.0

    @property
    def number_of_additional_points_either_side_of_order_line(self) -> 'int':
        """int: 'NumberOfAdditionalPointsEitherSideOfOrderLine' is the original name of this property."""

        temp = self.wrapped.NumberOfAdditionalPointsEitherSideOfOrderLine

        if temp is None:
            return 0

        return temp

    @number_of_additional_points_either_side_of_order_line.setter
    def number_of_additional_points_either_side_of_order_line(self, value: 'int'):
        self.wrapped.NumberOfAdditionalPointsEitherSideOfOrderLine = int(value) if value is not None else 0

    @property
    def reduce_number_of_result_points(self) -> 'bool':
        """bool: 'ReduceNumberOfResultPoints' is the original name of this property."""

        temp = self.wrapped.ReduceNumberOfResultPoints

        if temp is None:
            return False

        return temp

    @reduce_number_of_result_points.setter
    def reduce_number_of_result_points(self, value: 'bool'):
        self.wrapped.ReduceNumberOfResultPoints = bool(value) if value is not None else False

    @property
    def response_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType':
        """enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType: 'ResponseType' is the original name of this property."""

        temp = self.wrapped.ResponseType

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @response_type.setter
    def response_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.ResponseType = value

    @property
    def show_coupled_modes(self) -> 'bool':
        """bool: 'ShowCoupledModes' is the original name of this property."""

        temp = self.wrapped.ShowCoupledModes

        if temp is None:
            return False

        return temp

    @show_coupled_modes.setter
    def show_coupled_modes(self, value: 'bool'):
        self.wrapped.ShowCoupledModes = bool(value) if value is not None else False

    @property
    def show_total_response_for_multiple_excitations(self) -> 'bool':
        """bool: 'ShowTotalResponseForMultipleExcitations' is the original name of this property."""

        temp = self.wrapped.ShowTotalResponseForMultipleExcitations

        if temp is None:
            return False

        return temp

    @show_total_response_for_multiple_excitations.setter
    def show_total_response_for_multiple_excitations(self, value: 'bool'):
        self.wrapped.ShowTotalResponseForMultipleExcitations = bool(value) if value is not None else False

    @property
    def show_total_response_for_multiple_surfaces(self) -> 'bool':
        """bool: 'ShowTotalResponseForMultipleSurfaces' is the original name of this property."""

        temp = self.wrapped.ShowTotalResponseForMultipleSurfaces

        if temp is None:
            return False

        return temp

    @show_total_response_for_multiple_surfaces.setter
    def show_total_response_for_multiple_surfaces(self, value: 'bool'):
        self.wrapped.ShowTotalResponseForMultipleSurfaces = bool(value) if value is not None else False

    @property
    def speed_range_for_combining_excitations(self) -> '_4604.MultipleExcitationsSpeedRangeOption':
        """MultipleExcitationsSpeedRangeOption: 'SpeedRangeForCombiningExcitations' is the original name of this property."""

        temp = self.wrapped.SpeedRangeForCombiningExcitations

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_4604.MultipleExcitationsSpeedRangeOption)(value) if value is not None else None

    @speed_range_for_combining_excitations.setter
    def speed_range_for_combining_excitations(self, value: '_4604.MultipleExcitationsSpeedRangeOption'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SpeedRangeForCombiningExcitations = value

    @property
    def translation_or_rotation(self) -> '_1500.TranslationRotation':
        """TranslationRotation: 'TranslationOrRotation' is the original name of this property."""

        temp = self.wrapped.TranslationOrRotation

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1500.TranslationRotation)(value) if value is not None else None

    @translation_or_rotation.setter
    def translation_or_rotation(self, value: '_1500.TranslationRotation'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TranslationOrRotation = value

    @property
    def vector_magnitude_method(self) -> '_1486.ComplexMagnitudeMethod':
        """ComplexMagnitudeMethod: 'VectorMagnitudeMethod' is the original name of this property."""

        temp = self.wrapped.VectorMagnitudeMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1486.ComplexMagnitudeMethod)(value) if value is not None else None

    @vector_magnitude_method.setter
    def vector_magnitude_method(self, value: '_1486.ComplexMagnitudeMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.VectorMagnitudeMethod = value

    @property
    def whine_waterfall_export_option(self) -> '_4653.WhineWaterfallExportOption':
        """WhineWaterfallExportOption: 'WhineWaterfallExportOption' is the original name of this property."""

        temp = self.wrapped.WhineWaterfallExportOption

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_4653.WhineWaterfallExportOption)(value) if value is not None else None

    @whine_waterfall_export_option.setter
    def whine_waterfall_export_option(self, value: '_4653.WhineWaterfallExportOption'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.WhineWaterfallExportOption = value

    @property
    def data_scaling(self) -> '_1537.DataScalingOptions':
        """DataScalingOptions: 'DataScaling' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DataScaling

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def frequency_options(self) -> '_5692.FrequencyOptionsForHarmonicAnalysisResults':
        """FrequencyOptionsForHarmonicAnalysisResults: 'FrequencyOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FrequencyOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def harmonic_analysis_options(self) -> '_5704.HarmonicAnalysisOptions':
        """HarmonicAnalysisOptions: 'HarmonicAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicAnalysisOptions

        if temp is None:
            return None

        if _5704.HarmonicAnalysisOptions.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast harmonic_analysis_options to HarmonicAnalysisOptions. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def modal_contribution_view_options(self) -> '_2222.ModalContributionViewOptions':
        """ModalContributionViewOptions: 'ModalContributionViewOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModalContributionViewOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mode_view_options(self) -> '_2220.AdvancedTimeSteppingAnalysisForModulationModeViewOptions':
        """AdvancedTimeSteppingAnalysisForModulationModeViewOptions: 'ModeViewOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeViewOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def order_cuts_chart_settings(self) -> '_4606.OrderCutsChartSettings':
        """OrderCutsChartSettings: 'OrderCutsChartSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OrderCutsChartSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def reference_speed_options(self) -> '_5747.SpeedOptionsForHarmonicAnalysisResults':
        """SpeedOptionsForHarmonicAnalysisResults: 'ReferenceSpeedOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReferenceSpeedOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def result_location_selection_groups(self) -> '_5787.ResultLocationSelectionGroups':
        """ResultLocationSelectionGroups: 'ResultLocationSelectionGroups' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultLocationSelectionGroups

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_excitations(self) -> '_5782.ExcitationSourceSelectionGroup':
        """ExcitationSourceSelectionGroup: 'SelectedExcitations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SelectedExcitations

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def waterfall_chart_settings(self) -> '_4652.WaterfallChartSettings':
        """WaterfallChartSettings: 'WaterfallChartSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WaterfallChartSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def active_result_locations(self) -> 'List[_5788.ResultNodeSelection]':
        """List[ResultNodeSelection]: 'ActiveResultLocations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveResultLocations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def degrees_of_freedom(self) -> 'List[_1808.EnumWithBool[_1493.ResultOptionsFor3DVector]]':
        """List[EnumWithBool[ResultOptionsFor3DVector]]: 'DegreesOfFreedom' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DegreesOfFreedom

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

    def calculate_results(self):
        """ 'CalculateResults' is the original name of this method."""

        self.wrapped.CalculateResults()

    def clear_cached_results(self):
        """ 'ClearCachedResults' is the original name of this method."""

        self.wrapped.ClearCachedResults()

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
