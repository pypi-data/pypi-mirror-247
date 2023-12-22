﻿"""_1779.py

NamedTuple4
"""


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_NAMED_TUPLE_4 = python_net_import('SMT.MastaAPI.Utility.Generics', 'NamedTuple4')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedTuple4',)


T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')


class NamedTuple4(_0.APIBase, Generic[T1, T2, T3, T4]):
    """NamedTuple4

    This is a mastapy class.

    Generic Types:
        T1
        T2
        T3
        T4
    """

    TYPE = _NAMED_TUPLE_4

    def __init__(self, instance_to_wrap: 'NamedTuple4.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def item_1(self) -> 'T1':
        """T1: 'Item1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Item1

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def item_2(self) -> 'T2':
        """T2: 'Item2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Item2

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def item_3(self) -> 'T3':
        """T3: 'Item3' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Item3

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def item_4(self) -> 'T4':
        """T4: 'Item4' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Item4

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return ''

        return temp
