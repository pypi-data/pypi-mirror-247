﻿"""_1676.py

Rotatum
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_ROTATUM = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Rotatum')


__docformat__ = 'restructuredtext en'
__all__ = ('Rotatum',)


class Rotatum(_1573.MeasurementBase):
    """Rotatum

    This is a mastapy class.
    """

    TYPE = _ROTATUM

    def __init__(self, instance_to_wrap: 'Rotatum.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
