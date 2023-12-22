﻿"""_913.py

MicroGeometryGearSetDesignSpaceSearchStrategyDatabase
"""


from mastapy.math_utility.optimisation import _1508
from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_GEAR_SET_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'MicroGeometryGearSetDesignSpaceSearchStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryGearSetDesignSpaceSearchStrategyDatabase',)


class MicroGeometryGearSetDesignSpaceSearchStrategyDatabase(_1508.MicroGeometryDesignSpaceSearchStrategyDatabase):
    """MicroGeometryGearSetDesignSpaceSearchStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _MICRO_GEOMETRY_GEAR_SET_DESIGN_SPACE_SEARCH_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'MicroGeometryGearSetDesignSpaceSearchStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
