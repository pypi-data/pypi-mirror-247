﻿"""_1804.py

DutyCyclePropertySummaryForce
"""


from typing import Generic, TypeVar

from mastapy._internal import constructor
from mastapy.utility.property import _1803
from mastapy.utility.units_and_measurements.measurements import _1610
from mastapy._internal.python_net import python_net_import

_DUTY_CYCLE_PROPERTY_SUMMARY_FORCE = python_net_import('SMT.MastaAPI.Utility.Property', 'DutyCyclePropertySummaryForce')


__docformat__ = 'restructuredtext en'
__all__ = ('DutyCyclePropertySummaryForce',)


T = TypeVar('T')


class DutyCyclePropertySummaryForce(_1803.DutyCyclePropertySummary['_1610.Force', 'T'], Generic[T]):
    """DutyCyclePropertySummaryForce

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _DUTY_CYCLE_PROPERTY_SUMMARY_FORCE

    def __init__(self, instance_to_wrap: 'DutyCyclePropertySummaryForce.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def average_value(self) -> 'float':
        """float: 'AverageValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AverageValue

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_absolute_value(self) -> 'float':
        """float: 'MaximumAbsoluteValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumAbsoluteValue

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_value(self) -> 'float':
        """float: 'MaximumValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumValue

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_value(self) -> 'float':
        """float: 'MinimumValue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumValue

        if temp is None:
            return 0.0

        return temp
