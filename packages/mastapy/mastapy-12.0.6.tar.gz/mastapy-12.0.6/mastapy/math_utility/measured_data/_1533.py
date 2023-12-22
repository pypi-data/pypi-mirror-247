﻿"""_1533.py

GriddedSurfaceAccessor
"""


from typing import List

from clr import GetClrType

from mastapy._internal.python_net import python_net_import
from mastapy._internal import conversion, constructor
from mastapy.math_utility import _1481
from mastapy import _0

_ARRAY = python_net_import('System', 'Array')
_DOUBLE = python_net_import('System', 'Double')
_GRIDDED_SURFACE_ACCESSOR = python_net_import('SMT.MastaAPI.MathUtility.MeasuredData', 'GriddedSurfaceAccessor')


__docformat__ = 'restructuredtext en'
__all__ = ('GriddedSurfaceAccessor',)


class GriddedSurfaceAccessor(_0.APIBase):
    """GriddedSurfaceAccessor

    This is a mastapy class.
    """

    TYPE = _GRIDDED_SURFACE_ACCESSOR

    def __init__(self, instance_to_wrap: 'GriddedSurfaceAccessor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def create_new_from_gridded_data(self, x_values: 'List[float]', y_values: 'List[float]') -> 'GriddedSurfaceAccessor':
        """ 'CreateNewFromGriddedData' is the original name of this method.

        Args:
            x_values (List[float])
            y_values (List[float])

        Returns:
            mastapy.math_utility.measured_data.GriddedSurfaceAccessor
        """

        x_values = conversion.mp_to_pn_array_float(x_values)
        y_values = conversion.mp_to_pn_array_float(y_values)
        method_result = self.wrapped.CreateNewFromGriddedData.Overloads[_ARRAY[_DOUBLE], _ARRAY[_DOUBLE]](x_values, y_values)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_from_gridded_data_3d(self, x_values: 'List[float]', y_values: 'List[float]', z_values: 'List[List[float]]') -> 'GriddedSurfaceAccessor':
        """ 'CreateNewFromGriddedData' is the original name of this method.

        Args:
            x_values (List[float])
            y_values (List[float])
            z_values (List[List[float]])

        Returns:
            mastapy.math_utility.measured_data.GriddedSurfaceAccessor
        """

        x_values = conversion.mp_to_pn_array_float(x_values)
        y_values = conversion.mp_to_pn_array_float(y_values)
        z_values = conversion.mp_to_pn_list_float_2d(z_values)
        method_result = self.wrapped.CreateNewFromGriddedData.Overloads[_ARRAY[_DOUBLE], _ARRAY[_DOUBLE], GetClrType(_DOUBLE).MakeArrayType(2)](x_values, y_values, z_values)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_new_from_gridded_surface(self, grid: '_1481.GriddedSurface') -> 'GriddedSurfaceAccessor':
        """ 'CreateNewFromGriddedSurface' is the original name of this method.

        Args:
            grid (mastapy.math_utility.GriddedSurface)

        Returns:
            mastapy.math_utility.measured_data.GriddedSurfaceAccessor
        """

        method_result = self.wrapped.CreateNewFromGriddedSurface(grid.wrapped if grid else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def get_gridded_surface(self) -> '_1481.GriddedSurface':
        """ 'GetGriddedSurface' is the original name of this method.

        Returns:
            mastapy.math_utility.GriddedSurface
        """

        method_result = self.wrapped.GetGriddedSurface()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None
