﻿"""_6474.py

ExcelSheetDesignStateSelector
"""


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_EXCEL_SHEET_DESIGN_STATE_SELECTOR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DutyCycles.ExcelBatchDutyCycles', 'ExcelSheetDesignStateSelector')


__docformat__ = 'restructuredtext en'
__all__ = ('ExcelSheetDesignStateSelector',)


class ExcelSheetDesignStateSelector(_0.APIBase):
    """ExcelSheetDesignStateSelector

    This is a mastapy class.
    """

    TYPE = _EXCEL_SHEET_DESIGN_STATE_SELECTOR

    def __init__(self, instance_to_wrap: 'ExcelSheetDesignStateSelector.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def design_state(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'DesignState' is the original name of this property."""

        temp = self.wrapped.DesignState

        if temp is None:
            return ''

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else ''

    @design_state.setter
    def design_state(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.DesignState = value

    @property
    def sheet_name(self) -> 'str':
        """str: 'SheetName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SheetName

        if temp is None:
            return ''

        return temp
