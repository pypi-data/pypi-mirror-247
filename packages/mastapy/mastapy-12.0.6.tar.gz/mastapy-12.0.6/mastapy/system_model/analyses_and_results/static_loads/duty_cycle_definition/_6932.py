﻿"""_6932.py

SpeedInputOptions
"""


from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6930
from mastapy._internal.python_net import python_net_import

_SPEED_INPUT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition', 'SpeedInputOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('SpeedInputOptions',)


class SpeedInputOptions(_6930.PowerLoadInputOptions):
    """SpeedInputOptions

    This is a mastapy class.
    """

    TYPE = _SPEED_INPUT_OPTIONS

    def __init__(self, instance_to_wrap: 'SpeedInputOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
