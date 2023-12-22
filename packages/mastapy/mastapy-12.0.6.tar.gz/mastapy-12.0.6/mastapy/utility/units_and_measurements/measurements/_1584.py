﻿"""_1584.py

AngleVerySmall
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_ANGLE_VERY_SMALL = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'AngleVerySmall')


__docformat__ = 'restructuredtext en'
__all__ = ('AngleVerySmall',)


class AngleVerySmall(_1573.MeasurementBase):
    """AngleVerySmall

    This is a mastapy class.
    """

    TYPE = _ANGLE_VERY_SMALL

    def __init__(self, instance_to_wrap: 'AngleVerySmall.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
