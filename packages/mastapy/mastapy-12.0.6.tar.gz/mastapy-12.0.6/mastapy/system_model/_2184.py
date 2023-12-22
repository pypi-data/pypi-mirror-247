﻿"""_2184.py

SystemReporting
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements import _1573
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SYSTEM_REPORTING = python_net_import('SMT.MastaAPI.SystemModel', 'SystemReporting')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemReporting',)


class SystemReporting(_0.APIBase):
    """SystemReporting

    This is a mastapy class.
    """

    TYPE = _SYSTEM_REPORTING

    def __init__(self, instance_to_wrap: 'SystemReporting.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def current_date_and_time(self) -> 'str':
        """str: 'CurrentDateAndTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentDateAndTime

        if temp is None:
            return ''

        return temp

    @property
    def current_date_and_time_iso8601(self) -> 'str':
        """str: 'CurrentDateAndTimeISO8601' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CurrentDateAndTimeISO8601

        if temp is None:
            return ''

        return temp

    @property
    def masta_version(self) -> 'str':
        """str: 'MASTAVersion' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MASTAVersion

        if temp is None:
            return ''

        return temp

    @property
    def all_measurements(self) -> 'List[_1573.MeasurementBase]':
        """List[MeasurementBase]: 'AllMeasurements' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllMeasurements

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def measurements_not_using_si_unit(self) -> 'List[_1573.MeasurementBase]':
        """List[MeasurementBase]: 'MeasurementsNotUsingSIUnit' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeasurementsNotUsingSIUnit

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
