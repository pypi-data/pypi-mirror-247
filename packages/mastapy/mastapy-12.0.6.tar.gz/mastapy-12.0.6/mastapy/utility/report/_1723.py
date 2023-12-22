﻿"""_1723.py

CustomReportCadDrawing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility.cad_export import _1799
from mastapy.utility.report import _1739
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_CAD_DRAWING = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportCadDrawing')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportCadDrawing',)


class CustomReportCadDrawing(_1739.CustomReportNameableItem):
    """CustomReportCadDrawing

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_CAD_DRAWING

    def __init__(self, instance_to_wrap: 'CustomReportCadDrawing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def scale(self) -> 'float':
        """float: 'Scale' is the original name of this property."""

        temp = self.wrapped.Scale

        if temp is None:
            return 0.0

        return temp

    @scale.setter
    def scale(self, value: 'float'):
        self.wrapped.Scale = float(value) if value is not None else 0.0

    @property
    def stock_drawing(self) -> '_1799.StockDrawings':
        """StockDrawings: 'StockDrawing' is the original name of this property."""

        temp = self.wrapped.StockDrawing

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1799.StockDrawings)(value) if value is not None else None

    @stock_drawing.setter
    def stock_drawing(self, value: '_1799.StockDrawings'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.StockDrawing = value

    @property
    def use_stock_drawing(self) -> 'bool':
        """bool: 'UseStockDrawing' is the original name of this property."""

        temp = self.wrapped.UseStockDrawing

        if temp is None:
            return False

        return temp

    @use_stock_drawing.setter
    def use_stock_drawing(self, value: 'bool'):
        self.wrapped.UseStockDrawing = bool(value) if value is not None else False
