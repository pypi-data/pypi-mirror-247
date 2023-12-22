﻿"""_158.py

GeometryModellerLengthDimension
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis.geometry_modeller_link import _151
from mastapy._internal.python_net import python_net_import

_GEOMETRY_MODELLER_LENGTH_DIMENSION = python_net_import('SMT.MastaAPI.NodalAnalysis.GeometryModellerLink', 'GeometryModellerLengthDimension')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometryModellerLengthDimension',)


class GeometryModellerLengthDimension(_151.BaseGeometryModellerDimension):
    """GeometryModellerLengthDimension

    This is a mastapy class.
    """

    TYPE = _GEOMETRY_MODELLER_LENGTH_DIMENSION

    def __init__(self, instance_to_wrap: 'GeometryModellerLengthDimension.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return 0.0

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value is not None else 0.0
