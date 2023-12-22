﻿"""_1291.py

WindingMaterial
"""


from mastapy._internal import constructor
from mastapy.materials import _263
from mastapy._internal.python_net import python_net_import

_WINDING_MATERIAL = python_net_import('SMT.MastaAPI.ElectricMachines', 'WindingMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('WindingMaterial',)


class WindingMaterial(_263.Material):
    """WindingMaterial

    This is a mastapy class.
    """

    TYPE = _WINDING_MATERIAL

    def __init__(self, instance_to_wrap: 'WindingMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def relative_permeability(self) -> 'float':
        """float: 'RelativePermeability' is the original name of this property."""

        temp = self.wrapped.RelativePermeability

        if temp is None:
            return 0.0

        return temp

    @relative_permeability.setter
    def relative_permeability(self, value: 'float'):
        self.wrapped.RelativePermeability = float(value) if value is not None else 0.0

    @property
    def temperature_coefficient_for_winding_resistivity(self) -> 'float':
        """float: 'TemperatureCoefficientForWindingResistivity' is the original name of this property."""

        temp = self.wrapped.TemperatureCoefficientForWindingResistivity

        if temp is None:
            return 0.0

        return temp

    @temperature_coefficient_for_winding_resistivity.setter
    def temperature_coefficient_for_winding_resistivity(self, value: 'float'):
        self.wrapped.TemperatureCoefficientForWindingResistivity = float(value) if value is not None else 0.0

    @property
    def winding_resistivity_at_20_degrees_c(self) -> 'float':
        """float: 'WindingResistivityAt20DegreesC' is the original name of this property."""

        temp = self.wrapped.WindingResistivityAt20DegreesC

        if temp is None:
            return 0.0

        return temp

    @winding_resistivity_at_20_degrees_c.setter
    def winding_resistivity_at_20_degrees_c(self, value: 'float'):
        self.wrapped.WindingResistivityAt20DegreesC = float(value) if value is not None else 0.0
