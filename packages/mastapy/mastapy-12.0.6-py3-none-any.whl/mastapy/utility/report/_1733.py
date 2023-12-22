﻿"""_1733.py

CustomReportItemContainerCollection
"""


from typing import Generic, TypeVar

from mastapy.utility.report import _1734, _1735
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION = python_net_import('SMT.MastaAPI.Utility.Report', 'CustomReportItemContainerCollection')


__docformat__ = 'restructuredtext en'
__all__ = ('CustomReportItemContainerCollection',)


T = TypeVar('T', bound='_1735.CustomReportItemContainerCollectionItem')


class CustomReportItemContainerCollection(_1734.CustomReportItemContainerCollectionBase, Generic[T]):
    """CustomReportItemContainerCollection

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _CUSTOM_REPORT_ITEM_CONTAINER_COLLECTION

    def __init__(self, instance_to_wrap: 'CustomReportItemContainerCollection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
