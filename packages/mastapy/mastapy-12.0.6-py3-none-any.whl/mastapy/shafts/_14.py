﻿"""_14.py

GenericStressConcentrationFactor
"""


from mastapy._internal import constructor
from mastapy.shafts import _21
from mastapy._internal.python_net import python_net_import

_GENERIC_STRESS_CONCENTRATION_FACTOR = python_net_import('SMT.MastaAPI.Shafts', 'GenericStressConcentrationFactor')


__docformat__ = 'restructuredtext en'
__all__ = ('GenericStressConcentrationFactor',)


class GenericStressConcentrationFactor(_21.ShaftFeature):
    """GenericStressConcentrationFactor

    This is a mastapy class.
    """

    TYPE = _GENERIC_STRESS_CONCENTRATION_FACTOR

    def __init__(self, instance_to_wrap: 'GenericStressConcentrationFactor.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_factor(self) -> 'float':
        """float: 'BendingFactor' is the original name of this property."""

        temp = self.wrapped.BendingFactor

        if temp is None:
            return 0.0

        return temp

    @bending_factor.setter
    def bending_factor(self, value: 'float'):
        self.wrapped.BendingFactor = float(value) if value is not None else 0.0

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return 0.0

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value is not None else 0.0

    @property
    def tension_factor(self) -> 'float':
        """float: 'TensionFactor' is the original name of this property."""

        temp = self.wrapped.TensionFactor

        if temp is None:
            return 0.0

        return temp

    @tension_factor.setter
    def tension_factor(self, value: 'float'):
        self.wrapped.TensionFactor = float(value) if value is not None else 0.0

    @property
    def torsion_factor(self) -> 'float':
        """float: 'TorsionFactor' is the original name of this property."""

        temp = self.wrapped.TorsionFactor

        if temp is None:
            return 0.0

        return temp

    @torsion_factor.setter
    def torsion_factor(self, value: 'float'):
        self.wrapped.TorsionFactor = float(value) if value is not None else 0.0

    def add_new_generic_scf(self):
        """ 'AddNewGenericSCF' is the original name of this method."""

        self.wrapped.AddNewGenericSCF()
