﻿"""_4663.py

ComponentPerModeResult
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_COMPONENT_PER_MODE_RESULT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'ComponentPerModeResult')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentPerModeResult',)


class ComponentPerModeResult(_0.APIBase):
    """ComponentPerModeResult

    This is a mastapy class.
    """

    TYPE = _COMPONENT_PER_MODE_RESULT

    def __init__(self, instance_to_wrap: 'ComponentPerModeResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def mode_frequency(self) -> 'float':
        """float: 'ModeFrequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeFrequency

        if temp is None:
            return 0.0

        return temp

    @property
    def mode_id(self) -> 'int':
        """int: 'ModeID' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModeID

        if temp is None:
            return 0

        return temp

    @property
    def percentage_kinetic_energy(self) -> 'float':
        """float: 'PercentageKineticEnergy' is the original name of this property."""

        temp = self.wrapped.PercentageKineticEnergy

        if temp is None:
            return 0.0

        return temp

    @percentage_kinetic_energy.setter
    def percentage_kinetic_energy(self, value: 'float'):
        self.wrapped.PercentageKineticEnergy = float(value) if value is not None else 0.0

    @property
    def percentage_strain_energy(self) -> 'float':
        """float: 'PercentageStrainEnergy' is the original name of this property."""

        temp = self.wrapped.PercentageStrainEnergy

        if temp is None:
            return 0.0

        return temp

    @percentage_strain_energy.setter
    def percentage_strain_energy(self, value: 'float'):
        self.wrapped.PercentageStrainEnergy = float(value) if value is not None else 0.0
