﻿"""_2006.py

LoadedSphericalRollerThrustBearingResults
"""


from mastapy.bearings.bearing_results.rolling import _1992
from mastapy._internal.python_net import python_net_import

_LOADED_SPHERICAL_ROLLER_THRUST_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedSphericalRollerThrustBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedSphericalRollerThrustBearingResults',)


class LoadedSphericalRollerThrustBearingResults(_1992.LoadedRollerBearingResults):
    """LoadedSphericalRollerThrustBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_SPHERICAL_ROLLER_THRUST_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedSphericalRollerThrustBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
