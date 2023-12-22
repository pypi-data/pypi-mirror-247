﻿"""_6857.py

NamedSpeed
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_NAMED_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'NamedSpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedSpeed',)


class NamedSpeed(_0.APIBase):
    """NamedSpeed

    This is a mastapy class.
    """

    TYPE = _NAMED_SPEED

    def __init__(self, instance_to_wrap: 'NamedSpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property."""

        temp = self.wrapped.Name

        if temp is None:
            return ''

        return temp

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value is not None else ''

    @property
    def speed(self) -> 'float':
        """float: 'Speed' is the original name of this property."""

        temp = self.wrapped.Speed

        if temp is None:
            return 0.0

        return temp

    @speed.setter
    def speed(self, value: 'float'):
        self.wrapped.Speed = float(value) if value is not None else 0.0
