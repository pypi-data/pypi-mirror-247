﻿"""_2153.py

PlainJournalBearing
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs import _2093
from mastapy._internal.python_net import python_net_import

_PLAIN_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PlainJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlainJournalBearing',)


class PlainJournalBearing(_2093.DetailedBearing):
    """PlainJournalBearing

    This is a mastapy class.
    """

    TYPE = _PLAIN_JOURNAL_BEARING

    def __init__(self, instance_to_wrap: 'PlainJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def diametrical_clearance(self) -> 'float':
        """float: 'DiametricalClearance' is the original name of this property."""

        temp = self.wrapped.DiametricalClearance

        if temp is None:
            return 0.0

        return temp

    @diametrical_clearance.setter
    def diametrical_clearance(self, value: 'float'):
        self.wrapped.DiametricalClearance = float(value) if value is not None else 0.0

    @property
    def land_width(self) -> 'float':
        """float: 'LandWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LandWidth

        if temp is None:
            return 0.0

        return temp

    @property
    def land_width_to_diameter_ratio(self) -> 'float':
        """float: 'LandWidthToDiameterRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LandWidthToDiameterRatio

        if temp is None:
            return 0.0

        return temp
