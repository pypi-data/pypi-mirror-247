﻿"""_1731.py

CustomReportItem
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_ITEM = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportItem')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportItem',)


class CustomReportItem(_0.APIBase):
    """CustomReportItem

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_ITEM

    def __init__(self, instance_to_wrap: 'CustomReportItem.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_main_report_item(self) -> 'bool':
        """bool: 'IsMainReportItem' is the original name of this property."""

        temp = self.wrapped.IsMainReportItem

        if temp is None:
            return False

        return temp

    @is_main_report_item.setter
    def is_main_report_item(self, value: 'bool'):
        self.wrapped.IsMainReportItem = bool(value) if value is not None else False

    @property
    def item_type(self) -> 'str':
        """str: 'ItemType' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ItemType

        if temp is None:
            return ''

        return temp

    def add_condition(self):
        """ 'AddCondition' is the original name of this method."""

        self.wrapped.AddCondition()
