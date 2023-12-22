﻿"""_2017.py

LoadedThrustBallBearingResults
"""


from mastapy.bearings.bearing_results.rolling import _1965
from mastapy._internal.python_net import python_net_import

_LOADED_THRUST_BALL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedThrustBallBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedThrustBallBearingResults',)


class LoadedThrustBallBearingResults(_1965.LoadedBallBearingResults):
    """LoadedThrustBallBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_THRUST_BALL_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedThrustBallBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
