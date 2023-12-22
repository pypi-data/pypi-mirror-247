﻿"""_2054.py

MinimumLoad
"""


from typing import Optional

from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import _2059
from mastapy._internal.python_net import python_net_import

_MINIMUM_LOAD = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'MinimumLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('MinimumLoad',)


class MinimumLoad(_2059.SKFCalculationResult):
    """MinimumLoad

    This is a mastapy class.
    """

    TYPE = _MINIMUM_LOAD

    def __init__(self, instance_to_wrap: 'MinimumLoad.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def minimum_axial_load(self) -> 'Optional[float]':
        """Optional[float]: 'MinimumAxialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAxialLoad

        if temp is None:
            return None

        return temp

    @property
    def minimum_equivalent_load(self) -> 'Optional[float]':
        """Optional[float]: 'MinimumEquivalentLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumEquivalentLoad

        if temp is None:
            return None

        return temp

    @property
    def minimum_radial_load(self) -> 'Optional[float]':
        """Optional[float]: 'MinimumRadialLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumRadialLoad

        if temp is None:
            return None

        return temp

    @property
    def requirement_met(self) -> 'bool':
        """bool: 'RequirementMet' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RequirementMet

        if temp is None:
            return False

        return temp
