﻿"""_1619.py

Gradient
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_GRADIENT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Gradient')


__docformat__ = 'restructuredtext en'
__all__ = ('Gradient',)


class Gradient(_1573.MeasurementBase):
    """Gradient

    This is a mastapy class.
    """

    TYPE = _GRADIENT

    def __init__(self, instance_to_wrap: 'Gradient.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
