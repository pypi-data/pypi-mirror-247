﻿"""_4652.py

WaterfallChartSettings
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_WATERFALL_CHART_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'WaterfallChartSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('WaterfallChartSettings',)


class WaterfallChartSettings(_0.APIBase):
    """WaterfallChartSettings

    This is a mastapy class.
    """

    TYPE = _WATERFALL_CHART_SETTINGS

    def __init__(self, instance_to_wrap: 'WaterfallChartSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def three_d_view(self) -> 'bool':
        """bool: 'ThreeDView' is the original name of this property."""

        temp = self.wrapped.ThreeDView

        if temp is None:
            return False

        return temp

    @three_d_view.setter
    def three_d_view(self, value: 'bool'):
        self.wrapped.ThreeDView = bool(value) if value is not None else False

    @property
    def draw_modes_on_top_in_2d(self) -> 'bool':
        """bool: 'DrawModesOnTopIn2D' is the original name of this property."""

        temp = self.wrapped.DrawModesOnTopIn2D

        if temp is None:
            return False

        return temp

    @draw_modes_on_top_in_2d.setter
    def draw_modes_on_top_in_2d(self, value: 'bool'):
        self.wrapped.DrawModesOnTopIn2D = bool(value) if value is not None else False

    @property
    def draw_solid_floor(self) -> 'bool':
        """bool: 'DrawSolidFloor' is the original name of this property."""

        temp = self.wrapped.DrawSolidFloor

        if temp is None:
            return False

        return temp

    @draw_solid_floor.setter
    def draw_solid_floor(self, value: 'bool'):
        self.wrapped.DrawSolidFloor = bool(value) if value is not None else False

    @property
    def flip_axes(self) -> 'bool':
        """bool: 'FlipAxes' is the original name of this property."""

        temp = self.wrapped.FlipAxes

        if temp is None:
            return False

        return temp

    @flip_axes.setter
    def flip_axes(self, value: 'bool'):
        self.wrapped.FlipAxes = bool(value) if value is not None else False

    @property
    def invert_colours(self) -> 'bool':
        """bool: 'InvertColours' is the original name of this property."""

        temp = self.wrapped.InvertColours

        if temp is None:
            return False

        return temp

    @invert_colours.setter
    def invert_colours(self, value: 'bool'):
        self.wrapped.InvertColours = bool(value) if value is not None else False

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
