﻿"""_2462.py

PulleyFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2460
from mastapy._internal.python_net import python_net_import

_PULLEY_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'PulleyFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyFromCAD',)


class PulleyFromCAD(_2460.MountableComponentFromCAD):
    """PulleyFromCAD

    This is a mastapy class.
    """

    TYPE = _PULLEY_FROM_CAD

    def __init__(self, instance_to_wrap: 'PulleyFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def centre_distance(self) -> 'float':
        """float: 'CentreDistance' is the original name of this property."""

        temp = self.wrapped.CentreDistance

        if temp is None:
            return 0.0

        return temp

    @centre_distance.setter
    def centre_distance(self, value: 'float'):
        self.wrapped.CentreDistance = float(value) if value is not None else 0.0

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
