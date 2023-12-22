﻿"""_609.py

CylindricalManufacturedGearDutyCycle
"""


from mastapy.gears.analysis import _1210
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MANUFACTURED_GEAR_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalManufacturedGearDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalManufacturedGearDutyCycle',)


class CylindricalManufacturedGearDutyCycle(_1210.GearImplementationAnalysisDutyCycle):
    """CylindricalManufacturedGearDutyCycle

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_MANUFACTURED_GEAR_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'CylindricalManufacturedGearDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
