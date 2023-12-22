﻿"""_1726.py

CustomReportColumn
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1735
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_COLUMN = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportColumn')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportColumn',)


class CustomReportColumn(_1735.CustomReportItemContainerCollectionItem):
    """CustomReportColumn

    This is a mastapy class.
    """

    TYPE = _CUSTOM_REPORT_COLUMN

    def __init__(self, instance_to_wrap: 'CustomReportColumn.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def auto_width(self) -> 'bool':
        """bool: 'AutoWidth' is the original name of this property."""

        temp = self.wrapped.AutoWidth

        if temp is None:
            return False

        return temp

    @auto_width.setter
    def auto_width(self, value: 'bool'):
        self.wrapped.AutoWidth = bool(value) if value is not None else False

    @property
    def width(self) -> 'float':
        """float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return 0.0

        return temp

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value is not None else 0.0
