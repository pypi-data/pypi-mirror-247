﻿"""_914.py

MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase
"""


from mastapy.math_utility.optimisation import _1508
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_GEAR_SET_DUTY_CYCLE_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase',)


class MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase(_1508.MicroGeometryDesignSpaceSearchStrategyDatabase):
    """MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _MICRO_GEOMETRY_GEAR_SET_DUTY_CYCLE_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'MicroGeometryGearSetDutyCycleDesignSpaceSearchStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
