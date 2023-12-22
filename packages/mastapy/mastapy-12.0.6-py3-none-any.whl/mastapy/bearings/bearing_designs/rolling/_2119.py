﻿"""_2119.py

GeometricConstantsForSlidingFrictionalMoments
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEOMETRIC_CONSTANTS_FOR_SLIDING_FRICTIONAL_MOMENTS = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'GeometricConstantsForSlidingFrictionalMoments')


__docformat__ = 'restructuredtext en'
__all__ = ('GeometricConstantsForSlidingFrictionalMoments',)


class GeometricConstantsForSlidingFrictionalMoments(_0.APIBase):
    """GeometricConstantsForSlidingFrictionalMoments

    This is a mastapy class.
    """

    TYPE = _GEOMETRIC_CONSTANTS_FOR_SLIDING_FRICTIONAL_MOMENTS

    def __init__(self, instance_to_wrap: 'GeometricConstantsForSlidingFrictionalMoments.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def s1(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'S1' is the original name of this property."""

        temp = self.wrapped.S1

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @s1.setter
    def s1(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.S1 = value

    @property
    def s2(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'S2' is the original name of this property."""

        temp = self.wrapped.S2

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @s2.setter
    def s2(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.S2 = value

    @property
    def s3(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'S3' is the original name of this property."""

        temp = self.wrapped.S3

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @s3.setter
    def s3(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.S3 = value

    @property
    def s4(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'S4' is the original name of this property."""

        temp = self.wrapped.S4

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @s4.setter
    def s4(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.S4 = value

    @property
    def s5(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'S5' is the original name of this property."""

        temp = self.wrapped.S5

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @s5.setter
    def s5(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.S5 = value
