﻿"""_1600.py

Density
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_DENSITY = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Density')


__docformat__ = 'restructuredtext en'
__all__ = ('Density',)


class Density(_1573.MeasurementBase):
    """Density

    This is a mastapy class.
    """

    TYPE = _DENSITY

    def __init__(self, instance_to_wrap: 'Density.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
