﻿"""_2056.py

PermissibleAxialLoad
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_PERMISSIBLE_AXIAL_LOAD = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'PermissibleAxialLoad')


__docformat__ = 'restructuredtext en'
__all__ = ('PermissibleAxialLoad',)


class PermissibleAxialLoad(_0.APIBase):
    """PermissibleAxialLoad

    This is a mastapy class.
    """

    TYPE = _PERMISSIBLE_AXIAL_LOAD

    def __init__(self, instance_to_wrap: 'PermissibleAxialLoad.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def brief_periods(self) -> 'float':
        """float: 'BriefPeriods' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BriefPeriods

        if temp is None:
            return 0.0

        return temp

    @property
    def continuous(self) -> 'float':
        """float: 'Continuous' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Continuous

        if temp is None:
            return 0.0

        return temp

    @property
    def peak_loads(self) -> 'float':
        """float: 'PeakLoads' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PeakLoads

        if temp is None:
            return 0.0

        return temp
