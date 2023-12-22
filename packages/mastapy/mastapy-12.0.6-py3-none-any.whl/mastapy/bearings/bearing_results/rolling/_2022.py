﻿"""_2022.py

LoadedToroidalRollerBearingStripLoadResults
"""


from mastapy.bearings.bearing_results.rolling import _2005
from mastapy._internal.python_net import python_net_import

_LOADED_TOROIDAL_ROLLER_BEARING_STRIP_LOAD_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedToroidalRollerBearingStripLoadResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedToroidalRollerBearingStripLoadResults',)


class LoadedToroidalRollerBearingStripLoadResults(_2005.LoadedSphericalRollerRadialBearingStripLoadResults):
    """LoadedToroidalRollerBearingStripLoadResults

    This is a mastapy class.
    """

    TYPE = _LOADED_TOROIDAL_ROLLER_BEARING_STRIP_LOAD_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedToroidalRollerBearingStripLoadResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
