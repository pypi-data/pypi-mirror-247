﻿"""_2123.py

NonBarrelRollerBearing
"""


from typing import List

from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_designs.rolling import _2125, _2126, _2124
from mastapy._internal.python_net import python_net_import

_NON_BARREL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'NonBarrelRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('NonBarrelRollerBearing',)


class NonBarrelRollerBearing(_2124.RollerBearing):
    """NonBarrelRollerBearing

    This is a mastapy class.
    """

    TYPE = _NON_BARREL_ROLLER_BEARING

    def __init__(self, instance_to_wrap: 'NonBarrelRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def roller_end_radius(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'RollerEndRadius' is the original name of this property."""

        temp = self.wrapped.RollerEndRadius

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @roller_end_radius.setter
    def roller_end_radius(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.RollerEndRadius = value

    @property
    def roller_end_shape(self) -> '_2125.RollerEndShape':
        """RollerEndShape: 'RollerEndShape' is the original name of this property."""

        temp = self.wrapped.RollerEndShape

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2125.RollerEndShape)(value) if value is not None else None

    @roller_end_shape.setter
    def roller_end_shape(self, value: '_2125.RollerEndShape'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.RollerEndShape = value

    @property
    def ribs(self) -> 'List[_2126.RollerRibDetail]':
        """List[RollerRibDetail]: 'Ribs' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Ribs

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
