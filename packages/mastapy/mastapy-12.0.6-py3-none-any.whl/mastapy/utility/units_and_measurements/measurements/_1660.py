﻿"""_1660.py

PowerPerUnitTime
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_POWER_PER_UNIT_TIME = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'PowerPerUnitTime')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerPerUnitTime',)


class PowerPerUnitTime(_1573.MeasurementBase):
    """PowerPerUnitTime

    This is a mastapy class.
    """

    TYPE = _POWER_PER_UNIT_TIME

    def __init__(self, instance_to_wrap: 'PowerPerUnitTime.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
