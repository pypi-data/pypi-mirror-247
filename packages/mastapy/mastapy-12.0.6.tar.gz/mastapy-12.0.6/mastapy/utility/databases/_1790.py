﻿"""_1790.py

Database
"""


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy.utility.databases import _1792
from mastapy._internal.python_net import python_net_import

_DATABASE = python_net_import('SMT.MastaAPI.Utility.Databases', 'Database')


__docformat__ = 'restructuredtext en'
__all__ = ('Database',)


TKey = TypeVar('TKey', bound='_1792.DatabaseKey')
TValue = TypeVar('TValue', bound='_0.APIBase')


class Database(_0.APIBase, Generic[TKey, TValue]):
    """Database

    This is a mastapy class.

    Generic Types:
        TKey
        TValue
    """

    TYPE = _DATABASE

    def __init__(self, instance_to_wrap: 'Database.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def count(self) -> 'int':
        """int: 'Count' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Count

        if temp is None:
            return 0

        return temp

    def can_be_removed(self, item: 'TValue') -> 'bool':
        """ 'CanBeRemoved' is the original name of this method.

        Args:
            item (TValue)

        Returns:
            bool
        """

        method_result = self.wrapped.CanBeRemoved(item.wrapped if item else None)
        return method_result

    def get_all_items(self) -> 'List[TValue]':
        """ 'GetAllItems' is the original name of this method.

        Returns:
            List[TValue]
        """

        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetAllItems())
