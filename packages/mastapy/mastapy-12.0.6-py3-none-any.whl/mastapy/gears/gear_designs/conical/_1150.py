﻿"""_1150.py

ConicalMeshMisalignments
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MISALIGNMENTS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Conical', 'ConicalMeshMisalignments')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshMisalignments',)


class ConicalMeshMisalignments(_0.APIBase):
    """ConicalMeshMisalignments

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESH_MISALIGNMENTS

    def __init__(self, instance_to_wrap: 'ConicalMeshMisalignments.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def delta_e(self) -> 'float':
        """float: 'DeltaE' is the original name of this property."""

        temp = self.wrapped.DeltaE

        if temp is None:
            return 0.0

        return temp

    @delta_e.setter
    def delta_e(self, value: 'float'):
        self.wrapped.DeltaE = float(value) if value is not None else 0.0

    @property
    def delta_sigma(self) -> 'float':
        """float: 'DeltaSigma' is the original name of this property."""

        temp = self.wrapped.DeltaSigma

        if temp is None:
            return 0.0

        return temp

    @delta_sigma.setter
    def delta_sigma(self, value: 'float'):
        self.wrapped.DeltaSigma = float(value) if value is not None else 0.0

    @property
    def delta_xp(self) -> 'float':
        """float: 'DeltaXP' is the original name of this property."""

        temp = self.wrapped.DeltaXP

        if temp is None:
            return 0.0

        return temp

    @delta_xp.setter
    def delta_xp(self, value: 'float'):
        self.wrapped.DeltaXP = float(value) if value is not None else 0.0

    @property
    def delta_xw(self) -> 'float':
        """float: 'DeltaXW' is the original name of this property."""

        temp = self.wrapped.DeltaXW

        if temp is None:
            return 0.0

        return temp

    @delta_xw.setter
    def delta_xw(self, value: 'float'):
        self.wrapped.DeltaXW = float(value) if value is not None else 0.0
