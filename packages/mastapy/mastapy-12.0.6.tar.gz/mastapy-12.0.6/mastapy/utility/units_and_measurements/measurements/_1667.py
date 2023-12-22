﻿"""_1667.py

Pressure
"""


from mastapy.utility.units_and_measurements.measurements import _1682
from mastapy._internal.python_net import python_net_import

_PRESSURE = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Pressure')


__docformat__ = 'restructuredtext en'
__all__ = ('Pressure',)


class Pressure(_1682.Stress):
    """Pressure

    This is a mastapy class.
    """

    TYPE = _PRESSURE

    def __init__(self, instance_to_wrap: 'Pressure.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
