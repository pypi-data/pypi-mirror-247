﻿"""_1904.py

UserSpecifiedRollerRaceProfilePoint
"""


from mastapy._internal import constructor
from mastapy.bearings.roller_bearing_profiles import _1902
from mastapy._internal.python_net import python_net_import

_USER_SPECIFIED_ROLLER_RACE_PROFILE_POINT = python_net_import('SMT.MastaAPI.Bearings.RollerBearingProfiles', 'UserSpecifiedRollerRaceProfilePoint')


__docformat__ = 'restructuredtext en'
__all__ = ('UserSpecifiedRollerRaceProfilePoint',)


class UserSpecifiedRollerRaceProfilePoint(_1902.RollerRaceProfilePoint):
    """UserSpecifiedRollerRaceProfilePoint

    This is a mastapy class.
    """

    TYPE = _USER_SPECIFIED_ROLLER_RACE_PROFILE_POINT

    def __init__(self, instance_to_wrap: 'UserSpecifiedRollerRaceProfilePoint.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def race_analysis_deviation(self) -> 'float':
        """float: 'RaceAnalysisDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RaceAnalysisDeviation

        if temp is None:
            return 0.0

        return temp

    @property
    def roller_analysis_deviation(self) -> 'float':
        """float: 'RollerAnalysisDeviation' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RollerAnalysisDeviation

        if temp is None:
            return 0.0

        return temp
