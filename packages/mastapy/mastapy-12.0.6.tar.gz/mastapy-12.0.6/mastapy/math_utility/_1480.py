﻿"""_1480.py

GenericMatrix
"""


from typing import List, Generic, TypeVar

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GENERIC_MATRIX = python_net_import('SMT.MastaAPI.MathUtility', 'GenericMatrix')


__docformat__ = 'restructuredtext en'
__all__ = ('GenericMatrix',)


TElement = TypeVar('TElement', bound='object')
TMatrix = TypeVar('TMatrix', bound='GenericMatrix')


class GenericMatrix(_0.APIBase, Generic[TElement, TMatrix]):
    """GenericMatrix

    This is a mastapy class.

    Generic Types:
        TElement
        TMatrix
    """

    TYPE = _GENERIC_MATRIX

    def __init__(self, instance_to_wrap: 'GenericMatrix.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_columns(self) -> 'int':
        """int: 'NumberOfColumns' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfColumns

        if temp is None:
            return 0

        return temp

    @property
    def number_of_entries(self) -> 'int':
        """int: 'NumberOfEntries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfEntries

        if temp is None:
            return 0

        return temp

    @property
    def number_of_rows(self) -> 'int':
        """int: 'NumberOfRows' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfRows

        if temp is None:
            return 0

        return temp

    @property
    def data(self) -> 'List[TElement]':
        """List[TElement]: 'Data' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Data

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def get_column_at(self, index: 'int') -> 'List[TElement]':
        """ 'GetColumnAt' is the original name of this method.

        Args:
            index (int)

        Returns:
            List[TElement]
        """

        index = int(index)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetColumnAt(index if index else 0))

    def get_row_at(self, index: 'int') -> 'List[TElement]':
        """ 'GetRowAt' is the original name of this method.

        Args:
            index (int)

        Returns:
            List[TElement]
        """

        index = int(index)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.GetRowAt(index if index else 0))
