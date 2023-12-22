﻿"""_20.py

ShaftDamageResultsTableAndChart
"""


from mastapy.utility.enums import _1786
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.utility.report import _1724
from mastapy._internal.python_net import python_net_import

_SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART = python_net_import('SMT.MastaAPI.Shafts', 'ShaftDamageResultsTableAndChart')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftDamageResultsTableAndChart',)


class ShaftDamageResultsTableAndChart(_1724.CustomReportChart):
    """ShaftDamageResultsTableAndChart

    This is a mastapy class.
    """

    TYPE = _SHAFT_DAMAGE_RESULTS_TABLE_AND_CHART

    def __init__(self, instance_to_wrap: 'ShaftDamageResultsTableAndChart.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def display(self) -> '_1786.TableAndChartOptions':
        """TableAndChartOptions: 'Display' is the original name of this property."""

        temp = self.wrapped.Display

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1786.TableAndChartOptions)(value) if value is not None else None

    @display.setter
    def display(self, value: '_1786.TableAndChartOptions'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Display = value
