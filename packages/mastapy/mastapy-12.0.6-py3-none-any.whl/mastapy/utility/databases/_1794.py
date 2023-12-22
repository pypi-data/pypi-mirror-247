﻿"""_1794.py

NamedDatabase
"""


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy.utility.databases import _1795, _1797, _1796
from mastapy._internal.python_net import python_net_import

_NAMED_DATABASE = python_net_import('SMT.MastaAPI.Utility.Databases', 'NamedDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedDatabase',)


TValue = TypeVar('TValue', bound='_1795.NamedDatabaseItem')


class NamedDatabase(_1797.SQLDatabase['_1796.NamedKey', 'TValue'], Generic[TValue]):
    """NamedDatabase

    This is a mastapy class.

    Generic Types:
        TValue
    """

    TYPE = _NAMED_DATABASE

    def __init__(self, instance_to_wrap: 'NamedDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def create(self, name: 'str') -> 'TValue':
        """ 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            TValue
        """

        name = str(name)
        method_result = self.wrapped.Create(name if name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def duplicate(self, new_name: 'str', item: '_1795.NamedDatabaseItem') -> '_1795.NamedDatabaseItem':
        """ 'Duplicate' is the original name of this method.

        Args:
            new_name (str)
            item (mastapy.utility.databases.NamedDatabaseItem)

        Returns:
            mastapy.utility.databases.NamedDatabaseItem
        """

        new_name = str(new_name)
        method_result = self.wrapped.Duplicate(new_name if new_name else '', item.wrapped if item else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def get_value(self, name: 'str') -> 'TValue':
        """ 'GetValue' is the original name of this method.

        Args:
            name (str)

        Returns:
            TValue
        """

        name = str(name)
        method_result = self.wrapped.GetValue(name if name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def rename(self, item: '_1795.NamedDatabaseItem', new_name: 'str') -> 'bool':
        """ 'Rename' is the original name of this method.

        Args:
            item (mastapy.utility.databases.NamedDatabaseItem)
            new_name (str)

        Returns:
            bool
        """

        new_name = str(new_name)
        method_result = self.wrapped.Rename(item.wrapped if item else None, new_name if new_name else '')
        return method_result
