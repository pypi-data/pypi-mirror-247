﻿"""_1536.py

TwodimensionalFunctionLookupTable
"""


from mastapy.math_utility.measured_data import _1533, _1534
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_TWODIMENSIONAL_FUNCTION_LOOKUP_TABLE = python_net_import('SMT.MastaAPI.MathUtility.MeasuredData', 'TwodimensionalFunctionLookupTable')


__docformat__ = 'restructuredtext en'
__all__ = ('TwodimensionalFunctionLookupTable',)


class TwodimensionalFunctionLookupTable(_1534.LookupTableBase['TwodimensionalFunctionLookupTable']):
    """TwodimensionalFunctionLookupTable

    This is a mastapy class.
    """

    TYPE = _TWODIMENSIONAL_FUNCTION_LOOKUP_TABLE

    def __init__(self, instance_to_wrap: 'TwodimensionalFunctionLookupTable.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lookup_table(self) -> '_1533.GriddedSurfaceAccessor':
        """GriddedSurfaceAccessor: 'LookupTable' is the original name of this property."""

        temp = self.wrapped.LookupTable

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @lookup_table.setter
    def lookup_table(self, value: '_1533.GriddedSurfaceAccessor'):
        self.wrapped.LookupTable = value
