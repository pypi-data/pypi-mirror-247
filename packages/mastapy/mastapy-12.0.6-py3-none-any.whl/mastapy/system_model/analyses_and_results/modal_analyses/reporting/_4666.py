﻿"""_4666.py

PerModeResultsReport
"""


from mastapy.utility.enums import _1786
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility.report import _1724
from mastapy._internal.python_net import python_net_import

_PER_MODE_RESULTS_REPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'PerModeResultsReport')


__docformat__ = 'restructuredtext en'
__all__ = ('PerModeResultsReport',)


class PerModeResultsReport(_1724.CustomReportChart):
    """PerModeResultsReport

    This is a mastapy class.
    """

    TYPE = _PER_MODE_RESULTS_REPORT

    def __init__(self, instance_to_wrap: 'PerModeResultsReport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def display_option(self) -> '_1786.TableAndChartOptions':
        """TableAndChartOptions: 'DisplayOption' is the original name of this property."""

        temp = self.wrapped.DisplayOption

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1786.TableAndChartOptions)(value) if value is not None else None

    @display_option.setter
    def display_option(self, value: '_1786.TableAndChartOptions'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.DisplayOption = value

    @property
    def include_connected_parts_for_connections(self) -> 'bool':
        """bool: 'IncludeConnectedPartsForConnections' is the original name of this property."""

        temp = self.wrapped.IncludeConnectedPartsForConnections

        if temp is None:
            return False

        return temp

    @include_connected_parts_for_connections.setter
    def include_connected_parts_for_connections(self, value: 'bool'):
        self.wrapped.IncludeConnectedPartsForConnections = bool(value) if value is not None else False

    @property
    def maximum_number_of_modes_to_show_on_a_single_table_or_chart(self) -> 'int':
        """int: 'MaximumNumberOfModesToShowOnASingleTableOrChart' is the original name of this property."""

        temp = self.wrapped.MaximumNumberOfModesToShowOnASingleTableOrChart

        if temp is None:
            return 0

        return temp

    @maximum_number_of_modes_to_show_on_a_single_table_or_chart.setter
    def maximum_number_of_modes_to_show_on_a_single_table_or_chart(self, value: 'int'):
        self.wrapped.MaximumNumberOfModesToShowOnASingleTableOrChart = int(value) if value is not None else 0

    @property
    def show_all_modes(self) -> 'bool':
        """bool: 'ShowAllModes' is the original name of this property."""

        temp = self.wrapped.ShowAllModes

        if temp is None:
            return False

        return temp

    @show_all_modes.setter
    def show_all_modes(self, value: 'bool'):
        self.wrapped.ShowAllModes = bool(value) if value is not None else False

    @property
    def transpose_chart(self) -> 'bool':
        """bool: 'TransposeChart' is the original name of this property."""

        temp = self.wrapped.TransposeChart

        if temp is None:
            return False

        return temp

    @transpose_chart.setter
    def transpose_chart(self, value: 'bool'):
        self.wrapped.TransposeChart = bool(value) if value is not None else False

    @property
    def transpose_table(self) -> 'bool':
        """bool: 'TransposeTable' is the original name of this property."""

        temp = self.wrapped.TransposeTable

        if temp is None:
            return False

        return temp

    @transpose_table.setter
    def transpose_table(self, value: 'bool'):
        self.wrapped.TransposeTable = bool(value) if value is not None else False
