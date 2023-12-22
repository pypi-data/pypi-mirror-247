﻿"""_4300.py

DutyCycleResultsForSingleBearing
"""


from mastapy.bearings.bearing_results import _1912, _1920, _1923
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling import (
    _1955, _1962, _1970, _1986,
    _2009
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_RESULTS_FOR_SINGLE_BEARING = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'DutyCycleResultsForSingleBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCycleResultsForSingleBearing',)


class DutyCycleResultsForSingleBearing(_0.APIBase):
    """DutyCycleResultsForSingleBearing

    This is a mastapy class.
    """

    TYPE = _DUTY_CYCLE_RESULTS_FOR_SINGLE_BEARING

    def __init__(self, instance_to_wrap: 'DutyCycleResultsForSingleBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_results(self) -> '_1912.LoadedBearingDutyCycle':
        """LoadedBearingDutyCycle: 'DutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DutyCycleResults

        if temp is None:
            return None

        if _1912.LoadedBearingDutyCycle.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast duty_cycle_results to LoadedBearingDutyCycle. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
