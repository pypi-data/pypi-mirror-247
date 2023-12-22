﻿"""_2535.py

ClutchHalf
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2540
from mastapy._internal.python_net import python_net_import

_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchHalf',)


class ClutchHalf(_2540.CouplingHalf):
    """ClutchHalf

    This is a mastapy class.
    """

    TYPE = _CLUTCH_HALF

    def __init__(self, instance_to_wrap: 'ClutchHalf.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_mounted_on_shaft_outer(self) -> 'bool':
        """bool: 'IsMountedOnShaftOuter' is the original name of this property."""

        temp = self.wrapped.IsMountedOnShaftOuter

        if temp is None:
            return False

        return temp

    @is_mounted_on_shaft_outer.setter
    def is_mounted_on_shaft_outer(self, value: 'bool'):
        self.wrapped.IsMountedOnShaftOuter = bool(value) if value is not None else False
