﻿"""_1571.py

EnumUnit
"""


from mastapy.utility.units_and_measurements import _1578
from mastapy._internal.python_net import python_net_import

_ENUM_UNIT = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements', 'EnumUnit')


__docformat__ = 'restructuredtext en'
__all__ = ('EnumUnit',)


class EnumUnit(_1578.Unit):
    """EnumUnit

    This is a mastapy class.
    """

    TYPE = _ENUM_UNIT

    def __init__(self, instance_to_wrap: 'EnumUnit.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
