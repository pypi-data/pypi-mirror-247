﻿"""_1682.py

Stress
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_STRESS = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'Stress')


__docformat__ = 'restructuredtext en'
__all__ = ('Stress',)


class Stress(_1573.MeasurementBase):
    """Stress

    This is a mastapy class.
    """

    TYPE = _STRESS

    def __init__(self, instance_to_wrap: 'Stress.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
