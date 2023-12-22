﻿"""_1918.py

LoadedDetailedBearingResults
"""


from mastapy._internal import constructor
from mastapy.materials import _261
from mastapy.bearings.bearing_results import _1921
from mastapy._internal.python_net import python_net_import

_LOADED_DETAILED_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedDetailedBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedDetailedBearingResults',)


class LoadedDetailedBearingResults(_1921.LoadedNonLinearBearingResults):
    """LoadedDetailedBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_DETAILED_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedDetailedBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def lubricant_flow_rate(self) -> 'float':
        """float: 'LubricantFlowRate' is the original name of this property."""

        temp = self.wrapped.LubricantFlowRate

        if temp is None:
            return 0.0

        return temp

    @lubricant_flow_rate.setter
    def lubricant_flow_rate(self, value: 'float'):
        self.wrapped.LubricantFlowRate = float(value) if value is not None else 0.0

    @property
    def oil_sump_temperature(self) -> 'float':
        """float: 'OilSumpTemperature' is the original name of this property."""

        temp = self.wrapped.OilSumpTemperature

        if temp is None:
            return 0.0

        return temp

    @oil_sump_temperature.setter
    def oil_sump_temperature(self, value: 'float'):
        self.wrapped.OilSumpTemperature = float(value) if value is not None else 0.0

    @property
    def operating_air_temperature(self) -> 'float':
        """float: 'OperatingAirTemperature' is the original name of this property."""

        temp = self.wrapped.OperatingAirTemperature

        if temp is None:
            return 0.0

        return temp

    @operating_air_temperature.setter
    def operating_air_temperature(self, value: 'float'):
        self.wrapped.OperatingAirTemperature = float(value) if value is not None else 0.0

    @property
    def temperature_when_assembled(self) -> 'float':
        """float: 'TemperatureWhenAssembled' is the original name of this property."""

        temp = self.wrapped.TemperatureWhenAssembled

        if temp is None:
            return 0.0

        return temp

    @temperature_when_assembled.setter
    def temperature_when_assembled(self, value: 'float'):
        self.wrapped.TemperatureWhenAssembled = float(value) if value is not None else 0.0

    @property
    def lubrication(self) -> '_261.LubricationDetail':
        """LubricationDetail: 'Lubrication' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Lubrication

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
