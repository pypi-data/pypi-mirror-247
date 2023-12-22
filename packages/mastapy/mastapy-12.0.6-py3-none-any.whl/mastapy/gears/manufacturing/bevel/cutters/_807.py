﻿"""_807.py

PinionRoughCutter
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical import _1143
from mastapy._internal.python_net import python_net_import

_PINION_ROUGH_CUTTER = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel.Cutters', 'PinionRoughCutter')


__docformat__ = 'restructuredtext en'
__all__ = ('PinionRoughCutter',)


class PinionRoughCutter(_1143.ConicalGearCutter):
    """PinionRoughCutter

    This is a mastapy class.
    """

    TYPE = _PINION_ROUGH_CUTTER

    def __init__(self, instance_to_wrap: 'PinionRoughCutter.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def point_width(self) -> 'float':
        """float: 'PointWidth' is the original name of this property."""

        temp = self.wrapped.PointWidth

        if temp is None:
            return 0.0

        return temp

    @point_width.setter
    def point_width(self, value: 'float'):
        self.wrapped.PointWidth = float(value) if value is not None else 0.0
