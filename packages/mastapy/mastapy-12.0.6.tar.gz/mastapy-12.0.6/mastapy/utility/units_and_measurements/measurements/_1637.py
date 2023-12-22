﻿"""_1637.py

LengthVeryLong
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_LENGTH_VERY_LONG = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'LengthVeryLong')


__docformat__ = 'restructuredtext en'
__all__ = ('LengthVeryLong',)


class LengthVeryLong(_1573.MeasurementBase):
    """LengthVeryLong

    This is a mastapy class.
    """

    TYPE = _LENGTH_VERY_LONG

    def __init__(self, instance_to_wrap: 'LengthVeryLong.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
