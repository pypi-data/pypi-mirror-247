﻿"""_1894.py

RollerBearingConicalProfile
"""


from mastapy._internal import constructor
from mastapy.bearings.roller_bearing_profiles import _1900
from mastapy._internal.python_net import python_net_import

_ROLLER_BEARING_CONICAL_PROFILE = python_net_import('SMT.MastaAPI.Bearings.RollerBearingProfiles', 'RollerBearingConicalProfile')


__docformat__ = 'restructuredtext en'
__all__ = ('RollerBearingConicalProfile',)


class RollerBearingConicalProfile(_1900.RollerBearingProfile):
    """RollerBearingConicalProfile

    This is a mastapy class.
    """

    TYPE = _ROLLER_BEARING_CONICAL_PROFILE

    def __init__(self, instance_to_wrap: 'RollerBearingConicalProfile.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cone_angle(self) -> 'float':
        """float: 'ConeAngle' is the original name of this property."""

        temp = self.wrapped.ConeAngle

        if temp is None:
            return 0.0

        return temp

    @cone_angle.setter
    def cone_angle(self, value: 'float'):
        self.wrapped.ConeAngle = float(value) if value is not None else 0.0

    @property
    def deviation_offset(self) -> 'float':
        """float: 'DeviationOffset' is the original name of this property."""

        temp = self.wrapped.DeviationOffset

        if temp is None:
            return 0.0

        return temp

    @deviation_offset.setter
    def deviation_offset(self, value: 'float'):
        self.wrapped.DeviationOffset = float(value) if value is not None else 0.0

    @property
    def deviation_at_end_of_component(self) -> 'float':
        """float: 'DeviationAtEndOfComponent' is the original name of this property."""

        temp = self.wrapped.DeviationAtEndOfComponent

        if temp is None:
            return 0.0

        return temp

    @deviation_at_end_of_component.setter
    def deviation_at_end_of_component(self, value: 'float'):
        self.wrapped.DeviationAtEndOfComponent = float(value) if value is not None else 0.0
