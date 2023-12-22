﻿"""_1597.py

DamageRate
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_DAMAGE_RATE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'DamageRate')


__docformat__ = 'restructuredtext en'
__all__ = ('DamageRate',)


class DamageRate(_1573.MeasurementBase):
    """DamageRate

    This is a mastapy class.
    """

    TYPE = _DAMAGE_RATE

    def __init__(self, instance_to_wrap: 'DamageRate.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
