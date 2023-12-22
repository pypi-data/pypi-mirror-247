﻿"""_927.py

ParetoSpiralBevelGearSetOptimisationStrategyDatabase
"""


from mastapy.gears.gear_set_pareto_optimiser import _916
from mastapy._internal.python_net import python_net_import

_PARETO_SPIRAL_BEVEL_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'ParetoSpiralBevelGearSetOptimisationStrategyDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoSpiralBevelGearSetOptimisationStrategyDatabase',)


class ParetoSpiralBevelGearSetOptimisationStrategyDatabase(_916.ParetoConicalRatingOptimisationStrategyDatabase):
    """ParetoSpiralBevelGearSetOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE = _PARETO_SPIRAL_BEVEL_GEAR_SET_OPTIMISATION_STRATEGY_DATABASE

    def __init__(self, instance_to_wrap: 'ParetoSpiralBevelGearSetOptimisationStrategyDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
