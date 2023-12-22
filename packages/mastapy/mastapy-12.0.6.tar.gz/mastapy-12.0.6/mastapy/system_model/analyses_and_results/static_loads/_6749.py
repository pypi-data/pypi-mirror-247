﻿"""_6749.py

AllRingPinsManufacturingError
"""


from typing import List

from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.bearings.tolerances import _1882
from mastapy.system_model.analyses_and_results.static_loads import _6874
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ALL_RING_PINS_MANUFACTURING_ERROR = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AllRingPinsManufacturingError')


__docformat__ = 'restructuredtext en'
__all__ = ('AllRingPinsManufacturingError',)


class AllRingPinsManufacturingError(_0.APIBase):
    """AllRingPinsManufacturingError

    This is a mastapy class.
    """

    TYPE = _ALL_RING_PINS_MANUFACTURING_ERROR

    def __init__(self, instance_to_wrap: 'AllRingPinsManufacturingError.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def all_pins_roundness_chart(self) -> 'Image':
        """Image: 'AllPinsRoundnessChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllPinsRoundnessChart

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def angular_position_error_for_all_pins(self) -> 'float':
        """float: 'AngularPositionErrorForAllPins' is the original name of this property."""

        temp = self.wrapped.AngularPositionErrorForAllPins

        if temp is None:
            return 0.0

        return temp

    @angular_position_error_for_all_pins.setter
    def angular_position_error_for_all_pins(self, value: 'float'):
        self.wrapped.AngularPositionErrorForAllPins = float(value) if value is not None else 0.0

    @property
    def pin_diameter_error_for_all_pins(self) -> 'float':
        """float: 'PinDiameterErrorForAllPins' is the original name of this property."""

        temp = self.wrapped.PinDiameterErrorForAllPins

        if temp is None:
            return 0.0

        return temp

    @pin_diameter_error_for_all_pins.setter
    def pin_diameter_error_for_all_pins(self, value: 'float'):
        self.wrapped.PinDiameterErrorForAllPins = float(value) if value is not None else 0.0

    @property
    def radial_position_error_for_all_pins(self) -> 'float':
        """float: 'RadialPositionErrorForAllPins' is the original name of this property."""

        temp = self.wrapped.RadialPositionErrorForAllPins

        if temp is None:
            return 0.0

        return temp

    @radial_position_error_for_all_pins.setter
    def radial_position_error_for_all_pins(self, value: 'float'):
        self.wrapped.RadialPositionErrorForAllPins = float(value) if value is not None else 0.0

    @property
    def roundness_specification(self) -> '_1882.RoundnessSpecification':
        """RoundnessSpecification: 'RoundnessSpecification' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RoundnessSpecification

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ring_pin_manufacturing_errors(self) -> 'List[_6874.RingPinManufacturingError]':
        """List[RingPinManufacturingError]: 'RingPinManufacturingErrors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RingPinManufacturingErrors

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
