﻿"""_280.py

StressCyclesDataForTheContactSNCurveOfAPlasticMaterial
"""


from mastapy._internal import constructor
from mastapy.materials import _230
from mastapy._internal.python_net import python_net_import

_STRESS_CYCLES_DATA_FOR_THE_CONTACT_SN_CURVE_OF_A_PLASTIC_MATERIAL = python_net_import('SMT.MastaAPI.Materials', 'StressCyclesDataForTheContactSNCurveOfAPlasticMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('StressCyclesDataForTheContactSNCurveOfAPlasticMaterial',)


class StressCyclesDataForTheContactSNCurveOfAPlasticMaterial(_230.AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial):
    """StressCyclesDataForTheContactSNCurveOfAPlasticMaterial

    This is a mastapy class.
    """

    TYPE = _STRESS_CYCLES_DATA_FOR_THE_CONTACT_SN_CURVE_OF_A_PLASTIC_MATERIAL

    def __init__(self, instance_to_wrap: 'StressCyclesDataForTheContactSNCurveOfAPlasticMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_fatigue_strength_under_pulsating_stress(self) -> 'float':
        """float: 'ContactFatigueStrengthUnderPulsatingStress' is the original name of this property."""

        temp = self.wrapped.ContactFatigueStrengthUnderPulsatingStress

        if temp is None:
            return 0.0

        return temp

    @contact_fatigue_strength_under_pulsating_stress.setter
    def contact_fatigue_strength_under_pulsating_stress(self, value: 'float'):
        self.wrapped.ContactFatigueStrengthUnderPulsatingStress = float(value) if value is not None else 0.0
