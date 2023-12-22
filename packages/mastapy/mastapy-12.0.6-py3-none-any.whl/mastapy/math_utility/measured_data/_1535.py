﻿"""_1535.py

OnedimensionalFunctionLookupTable
"""


from mastapy.math_utility import _1501
from mastapy._internal import constructor
from mastapy.math_utility.measured_data import _1534
from mastapy._internal.python_net import python_net_import

_ONEDIMENSIONAL_FUNCTION_LOOKUP_TABLE = python_net_import('SMT.MastaAPI.MathUtility.MeasuredData', 'OnedimensionalFunctionLookupTable')


__docformat__ = 'restructuredtext en'
__all__ = ('OnedimensionalFunctionLookupTable',)


class OnedimensionalFunctionLookupTable(_1534.LookupTableBase['OnedimensionalFunctionLookupTable']):
    """OnedimensionalFunctionLookupTable

    This is a mastapy class.
    """

    TYPE = _ONEDIMENSIONAL_FUNCTION_LOOKUP_TABLE

    def __init__(self, instance_to_wrap: 'OnedimensionalFunctionLookupTable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lookup_table(self) -> '_1501.Vector2DListAccessor':
        """Vector2DListAccessor: 'LookupTable' is the original name of this property."""

        temp = self.wrapped.LookupTable

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @lookup_table.setter
    def lookup_table(self, value: '_1501.Vector2DListAccessor'):
        self.wrapped.LookupTable = value
