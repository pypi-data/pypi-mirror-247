﻿"""_2050.py

GreaseLifeAndRelubricationInterval
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import (
    _2049, _2051, _2052, _2059
)
from mastapy._internal.python_net import python_net_import

_GREASE_LIFE_AND_RELUBRICATION_INTERVAL = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'GreaseLifeAndRelubricationInterval')


__docformat__ = 'restructuredtext en'
__all__ = ('GreaseLifeAndRelubricationInterval',)


class GreaseLifeAndRelubricationInterval(_2059.SKFCalculationResult):
    """GreaseLifeAndRelubricationInterval

    This is a mastapy class.
    """

    TYPE = _GREASE_LIFE_AND_RELUBRICATION_INTERVAL

    def __init__(self, instance_to_wrap: 'GreaseLifeAndRelubricationInterval.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def speed_factor(self) -> 'float':
        """float: 'SpeedFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpeedFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def grease(self) -> '_2049.Grease':
        """Grease: 'Grease' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Grease

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def grease_quantity(self) -> '_2051.GreaseQuantity':
        """GreaseQuantity: 'GreaseQuantity' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GreaseQuantity

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def initial_fill(self) -> '_2052.InitialFill':
        """InitialFill: 'InitialFill' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InitialFill

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
