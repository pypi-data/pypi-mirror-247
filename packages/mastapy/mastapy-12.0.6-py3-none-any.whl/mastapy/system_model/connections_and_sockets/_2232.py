﻿"""_2232.py

CVTBeltConnection
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import _2227
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnection',)


class CVTBeltConnection(_2227.BeltConnection):
    """CVTBeltConnection

    This is a mastapy class.
    """

    TYPE = _CVT_BELT_CONNECTION

    def __init__(self, instance_to_wrap: 'CVTBeltConnection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def belt_efficiency(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BeltEfficiency' is the original name of this property."""

        temp = self.wrapped.BeltEfficiency

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @belt_efficiency.setter
    def belt_efficiency(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BeltEfficiency = value
