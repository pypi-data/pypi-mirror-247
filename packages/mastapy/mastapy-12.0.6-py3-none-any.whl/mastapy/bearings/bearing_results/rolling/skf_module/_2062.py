﻿"""_2062.py

StaticSafetyFactors
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _2059
from mastapy._internal.python_net import python_net_import

_STATIC_SAFETY_FACTORS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'StaticSafetyFactors')


__docformat__ = 'restructuredtext en'
__all__ = ('StaticSafetyFactors',)


class StaticSafetyFactors(_2059.SKFCalculationResult):
    """StaticSafetyFactors

    This is a mastapy class.
    """

    TYPE = _STATIC_SAFETY_FACTORS

    def __init__(self, instance_to_wrap: 'StaticSafetyFactors.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def equivalent_static_load(self) -> 'float':
        """float: 'EquivalentStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EquivalentStaticLoad

        if temp is None:
            return 0.0

        return temp

    @property
    def static_safety_factor(self) -> 'float':
        """float: 'StaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StaticSafetyFactor

        if temp is None:
            return 0.0

        return temp
