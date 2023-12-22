﻿"""_1062.py

Scuffing
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value
from mastapy.gears.gear_designs.cylindrical import _1063, _1064, _1065
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.utility import _1554
from mastapy._internal.python_net import python_net_import

_SCUFFING = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'Scuffing')


__docformat__ = 'restructuredtext en'
__all__ = ('Scuffing',)


class Scuffing(_1554.IndependentReportablePropertiesBase['Scuffing']):
    """Scuffing

    This is a mastapy class.
    """

    TYPE = _SCUFFING

    def __init__(self, instance_to_wrap: 'Scuffing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bulk_tooth_temperature_of_test_gears_flash_temperature_method(self) -> 'float':
        """float: 'BulkToothTemperatureOfTestGearsFlashTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.BulkToothTemperatureOfTestGearsFlashTemperatureMethod

        if temp is None:
            return 0.0

        return temp

    @bulk_tooth_temperature_of_test_gears_flash_temperature_method.setter
    def bulk_tooth_temperature_of_test_gears_flash_temperature_method(self, value: 'float'):
        self.wrapped.BulkToothTemperatureOfTestGearsFlashTemperatureMethod = float(value) if value is not None else 0.0

    @property
    def bulk_tooth_temperature_of_test_gears_integral_temperature_method(self) -> 'float':
        """float: 'BulkToothTemperatureOfTestGearsIntegralTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.BulkToothTemperatureOfTestGearsIntegralTemperatureMethod

        if temp is None:
            return 0.0

        return temp

    @bulk_tooth_temperature_of_test_gears_integral_temperature_method.setter
    def bulk_tooth_temperature_of_test_gears_integral_temperature_method(self, value: 'float'):
        self.wrapped.BulkToothTemperatureOfTestGearsIntegralTemperatureMethod = float(value) if value is not None else 0.0

    @property
    def coefficient_of_friction_method_flash_temperature_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods':
        """enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods: 'CoefficientOfFrictionMethodFlashTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.CoefficientOfFrictionMethodFlashTemperatureMethod

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @coefficient_of_friction_method_flash_temperature_method.setter
    def coefficient_of_friction_method_flash_temperature_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.CoefficientOfFrictionMethodFlashTemperatureMethod = value

    @property
    def contact_time_at_high_velocity(self) -> 'float':
        """float: 'ContactTimeAtHighVelocity' is the original name of this property."""

        temp = self.wrapped.ContactTimeAtHighVelocity

        if temp is None:
            return 0.0

        return temp

    @contact_time_at_high_velocity.setter
    def contact_time_at_high_velocity(self, value: 'float'):
        self.wrapped.ContactTimeAtHighVelocity = float(value) if value is not None else 0.0

    @property
    def contact_time_at_medium_velocity(self) -> 'float':
        """float: 'ContactTimeAtMediumVelocity' is the original name of this property."""

        temp = self.wrapped.ContactTimeAtMediumVelocity

        if temp is None:
            return 0.0

        return temp

    @contact_time_at_medium_velocity.setter
    def contact_time_at_medium_velocity(self, value: 'float'):
        self.wrapped.ContactTimeAtMediumVelocity = float(value) if value is not None else 0.0

    @property
    def estimate_oil_test_results_for_long_contact_times(self) -> 'bool':
        """bool: 'EstimateOilTestResultsForLongContactTimes' is the original name of this property."""

        temp = self.wrapped.EstimateOilTestResultsForLongContactTimes

        if temp is None:
            return False

        return temp

    @estimate_oil_test_results_for_long_contact_times.setter
    def estimate_oil_test_results_for_long_contact_times(self, value: 'bool'):
        self.wrapped.EstimateOilTestResultsForLongContactTimes = bool(value) if value is not None else False

    @property
    def estimate_tooth_temperature(self) -> 'bool':
        """bool: 'EstimateToothTemperature' is the original name of this property."""

        temp = self.wrapped.EstimateToothTemperature

        if temp is None:
            return False

        return temp

    @estimate_tooth_temperature.setter
    def estimate_tooth_temperature(self, value: 'bool'):
        self.wrapped.EstimateToothTemperature = bool(value) if value is not None else False

    @property
    def maximum_flash_temperature_of_test_gears_flash_temperature_method(self) -> 'float':
        """float: 'MaximumFlashTemperatureOfTestGearsFlashTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.MaximumFlashTemperatureOfTestGearsFlashTemperatureMethod

        if temp is None:
            return 0.0

        return temp

    @maximum_flash_temperature_of_test_gears_flash_temperature_method.setter
    def maximum_flash_temperature_of_test_gears_flash_temperature_method(self, value: 'float'):
        self.wrapped.MaximumFlashTemperatureOfTestGearsFlashTemperatureMethod = float(value) if value is not None else 0.0

    @property
    def mean_coefficient_of_friction_flash_temperature_method(self) -> 'float':
        """float: 'MeanCoefficientOfFrictionFlashTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.MeanCoefficientOfFrictionFlashTemperatureMethod

        if temp is None:
            return 0.0

        return temp

    @mean_coefficient_of_friction_flash_temperature_method.setter
    def mean_coefficient_of_friction_flash_temperature_method(self, value: 'float'):
        self.wrapped.MeanCoefficientOfFrictionFlashTemperatureMethod = float(value) if value is not None else 0.0

    @property
    def mean_flash_temperature_of_test_gears_integral_temperature_method(self) -> 'float':
        """float: 'MeanFlashTemperatureOfTestGearsIntegralTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.MeanFlashTemperatureOfTestGearsIntegralTemperatureMethod

        if temp is None:
            return 0.0

        return temp

    @mean_flash_temperature_of_test_gears_integral_temperature_method.setter
    def mean_flash_temperature_of_test_gears_integral_temperature_method(self, value: 'float'):
        self.wrapped.MeanFlashTemperatureOfTestGearsIntegralTemperatureMethod = float(value) if value is not None else 0.0

    @property
    def scuffing_temperature_at_high_velocity(self) -> 'float':
        """float: 'ScuffingTemperatureAtHighVelocity' is the original name of this property."""

        temp = self.wrapped.ScuffingTemperatureAtHighVelocity

        if temp is None:
            return 0.0

        return temp

    @scuffing_temperature_at_high_velocity.setter
    def scuffing_temperature_at_high_velocity(self, value: 'float'):
        self.wrapped.ScuffingTemperatureAtHighVelocity = float(value) if value is not None else 0.0

    @property
    def scuffing_temperature_at_medium_velocity(self) -> 'float':
        """float: 'ScuffingTemperatureAtMediumVelocity' is the original name of this property."""

        temp = self.wrapped.ScuffingTemperatureAtMediumVelocity

        if temp is None:
            return 0.0

        return temp

    @scuffing_temperature_at_medium_velocity.setter
    def scuffing_temperature_at_medium_velocity(self, value: 'float'):
        self.wrapped.ScuffingTemperatureAtMediumVelocity = float(value) if value is not None else 0.0

    @property
    def scuffing_temperature_method_agma(self) -> '_1064.ScuffingTemperatureMethodsAGMA':
        """ScuffingTemperatureMethodsAGMA: 'ScuffingTemperatureMethodAGMA' is the original name of this property."""

        temp = self.wrapped.ScuffingTemperatureMethodAGMA

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1064.ScuffingTemperatureMethodsAGMA)(value) if value is not None else None

    @scuffing_temperature_method_agma.setter
    def scuffing_temperature_method_agma(self, value: '_1064.ScuffingTemperatureMethodsAGMA'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ScuffingTemperatureMethodAGMA = value

    @property
    def scuffing_temperature_method_iso(self) -> '_1065.ScuffingTemperatureMethodsISO':
        """ScuffingTemperatureMethodsISO: 'ScuffingTemperatureMethodISO' is the original name of this property."""

        temp = self.wrapped.ScuffingTemperatureMethodISO

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1065.ScuffingTemperatureMethodsISO)(value) if value is not None else None

    @scuffing_temperature_method_iso.setter
    def scuffing_temperature_method_iso(self, value: '_1065.ScuffingTemperatureMethodsISO'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ScuffingTemperatureMethodISO = value

    @property
    def user_input_scuffing_integral_temperature_for_long_contact_times(self) -> 'float':
        """float: 'UserInputScuffingIntegralTemperatureForLongContactTimes' is the original name of this property."""

        temp = self.wrapped.UserInputScuffingIntegralTemperatureForLongContactTimes

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_integral_temperature_for_long_contact_times.setter
    def user_input_scuffing_integral_temperature_for_long_contact_times(self, value: 'float'):
        self.wrapped.UserInputScuffingIntegralTemperatureForLongContactTimes = float(value) if value is not None else 0.0

    @property
    def user_input_scuffing_temperature_flash_temperature_method(self) -> 'float':
        """float: 'UserInputScuffingTemperatureFlashTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.UserInputScuffingTemperatureFlashTemperatureMethod

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_temperature_flash_temperature_method.setter
    def user_input_scuffing_temperature_flash_temperature_method(self, value: 'float'):
        self.wrapped.UserInputScuffingTemperatureFlashTemperatureMethod = float(value) if value is not None else 0.0

    @property
    def user_input_scuffing_temperature_integral_temperature_method(self) -> 'float':
        """float: 'UserInputScuffingTemperatureIntegralTemperatureMethod' is the original name of this property."""

        temp = self.wrapped.UserInputScuffingTemperatureIntegralTemperatureMethod

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_temperature_integral_temperature_method.setter
    def user_input_scuffing_temperature_integral_temperature_method(self, value: 'float'):
        self.wrapped.UserInputScuffingTemperatureIntegralTemperatureMethod = float(value) if value is not None else 0.0

    @property
    def user_input_scuffing_temperature_for_long_contact_times(self) -> 'float':
        """float: 'UserInputScuffingTemperatureForLongContactTimes' is the original name of this property."""

        temp = self.wrapped.UserInputScuffingTemperatureForLongContactTimes

        if temp is None:
            return 0.0

        return temp

    @user_input_scuffing_temperature_for_long_contact_times.setter
    def user_input_scuffing_temperature_for_long_contact_times(self, value: 'float'):
        self.wrapped.UserInputScuffingTemperatureForLongContactTimes = float(value) if value is not None else 0.0
