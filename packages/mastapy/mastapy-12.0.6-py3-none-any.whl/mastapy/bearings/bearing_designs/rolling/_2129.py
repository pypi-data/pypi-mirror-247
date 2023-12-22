﻿"""_2129.py

SKFSealFrictionalMomentConstants
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings import _1862
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SKF_SEAL_FRICTIONAL_MOMENT_CONSTANTS = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'SKFSealFrictionalMomentConstants')


__docformat__ = 'restructuredtext en'
__all__ = ('SKFSealFrictionalMomentConstants',)


class SKFSealFrictionalMomentConstants(_0.APIBase):
    """SKFSealFrictionalMomentConstants

    This is a mastapy class.
    """

    TYPE = _SKF_SEAL_FRICTIONAL_MOMENT_CONSTANTS

    def __init__(self, instance_to_wrap: 'SKFSealFrictionalMomentConstants.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def ks1(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'KS1' is the original name of this property."""

        temp = self.wrapped.KS1

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @ks1.setter
    def ks1(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.KS1 = value

    @property
    def ks2(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'KS2' is the original name of this property."""

        temp = self.wrapped.KS2

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @ks2.setter
    def ks2(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.KS2 = value

    @property
    def seal_counterface_diameter(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'SealCounterfaceDiameter' is the original name of this property."""

        temp = self.wrapped.SealCounterfaceDiameter

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @seal_counterface_diameter.setter
    def seal_counterface_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.SealCounterfaceDiameter = value

    @property
    def seal_location(self) -> 'overridable.Overridable_SealLocation':
        """overridable.Overridable_SealLocation: 'SealLocation' is the original name of this property."""

        temp = self.wrapped.SealLocation

        if temp is None:
            return None

        value = overridable.Overridable_SealLocation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @seal_location.setter
    def seal_location(self, value: 'overridable.Overridable_SealLocation.implicit_type()'):
        wrapper_type = overridable.Overridable_SealLocation.wrapper_type()
        enclosed_type = overridable.Overridable_SealLocation.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.SealLocation = value

    @property
    def beta(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'Beta' is the original name of this property."""

        temp = self.wrapped.Beta

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @beta.setter
    def beta(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.Beta = value
