﻿"""_1630.py

Jerk
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_JERK = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Jerk')


__docformat__ = 'restructuredtext en'
__all__ = ('Jerk',)


class Jerk(_1573.MeasurementBase):
    """Jerk

    This is a mastapy class.
    """

    TYPE = _JERK

    def __init__(self, instance_to_wrap: 'Jerk.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
