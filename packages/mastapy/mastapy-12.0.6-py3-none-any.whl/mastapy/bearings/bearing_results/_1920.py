﻿"""_1920.py

LoadedNonLinearBearingDutyCycleResults
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results import _1912
from mastapy._internal.python_net import python_net_import

_LOADED_NON_LINEAR_BEARING_DUTY_CYCLE_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedNonLinearBearingDutyCycleResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNonLinearBearingDutyCycleResults',)


class LoadedNonLinearBearingDutyCycleResults(_1912.LoadedBearingDutyCycle):
    """LoadedNonLinearBearingDutyCycleResults

    This is a mastapy class.
    """

    TYPE = _LOADED_NON_LINEAR_BEARING_DUTY_CYCLE_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedNonLinearBearingDutyCycleResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def total_power_loss(self) -> 'float':
        """float: 'TotalPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalPowerLoss

        if temp is None:
            return 0.0

        return temp
