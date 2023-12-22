﻿"""_2453.py

ConnectorFromCAD
"""


from mastapy.system_model.part_model.import_from_cad import _2459, _2460
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.python_net import python_net_import

_CONNECTOR_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'ConnectorFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectorFromCAD',)


class ConnectorFromCAD(_2460.MountableComponentFromCAD):
    """ConnectorFromCAD

    This is a mastapy class.
    """

    TYPE = _CONNECTOR_FROM_CAD

    def __init__(self, instance_to_wrap: 'ConnectorFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mounting(self) -> '_2459.HousedOrMounted':
        """HousedOrMounted: 'Mounting' is the original name of this property."""

        temp = self.wrapped.Mounting

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2459.HousedOrMounted)(value) if value is not None else None

    @mounting.setter
    def mounting(self, value: '_2459.HousedOrMounted'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Mounting = value
