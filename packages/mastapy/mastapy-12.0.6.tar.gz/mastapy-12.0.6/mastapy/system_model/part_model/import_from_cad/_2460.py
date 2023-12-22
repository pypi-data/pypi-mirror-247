﻿"""_2460.py

MountableComponentFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2451
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'MountableComponentFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('MountableComponentFromCAD',)


class MountableComponentFromCAD(_2451.ComponentFromCAD):
    """MountableComponentFromCAD

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_FROM_CAD

    def __init__(self, instance_to_wrap: 'MountableComponentFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def offset(self) -> 'float':
        """float: 'Offset' is the original name of this property."""

        temp = self.wrapped.Offset

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    def offset(self, value: 'float'):
        self.wrapped.Offset = float(value) if value is not None else 0.0
