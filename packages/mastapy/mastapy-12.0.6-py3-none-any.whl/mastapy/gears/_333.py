﻿"""_333.py

NamedPlanetAngle
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_NAMED_PLANET_ANGLE = python_net_import('SMT.MastaAPI.Gears', 'NamedPlanetAngle')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedPlanetAngle',)


class NamedPlanetAngle(_0.APIBase):
    """NamedPlanetAngle

    This is a mastapy class.
    """

    TYPE = _NAMED_PLANET_ANGLE

    def __init__(self, instance_to_wrap: 'NamedPlanetAngle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planet_angle(self) -> 'float':
        """float: 'PlanetAngle' is the original name of this property."""

        temp = self.wrapped.PlanetAngle

        if temp is None:
            return 0.0

        return temp

    @planet_angle.setter
    def planet_angle(self, value: 'float'):
        self.wrapped.PlanetAngle = float(value) if value is not None else 0.0
