﻿"""_2464.py

RollingBearingFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2453
from mastapy._internal.python_net import python_net_import

_ROLLING_BEARING_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'RollingBearingFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearingFromCAD',)


class RollingBearingFromCAD(_2453.ConnectorFromCAD):
    """RollingBearingFromCAD

    This is a mastapy class.
    """

    TYPE = _ROLLING_BEARING_FROM_CAD

    def __init__(self, instance_to_wrap: 'RollingBearingFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bore(self) -> 'float':
        """float: 'Bore' is the original name of this property."""

        temp = self.wrapped.Bore

        if temp is None:
            return 0.0

        return temp

    @bore.setter
    def bore(self, value: 'float'):
        self.wrapped.Bore = float(value) if value is not None else 0.0

    @property
    def outer_diameter(self) -> 'float':
        """float: 'OuterDiameter' is the original name of this property."""

        temp = self.wrapped.OuterDiameter

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    def outer_diameter(self, value: 'float'):
        self.wrapped.OuterDiameter = float(value) if value is not None else 0.0

    @property
    def width(self) -> 'float':
        """float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return 0.0

        return temp

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value is not None else 0.0
