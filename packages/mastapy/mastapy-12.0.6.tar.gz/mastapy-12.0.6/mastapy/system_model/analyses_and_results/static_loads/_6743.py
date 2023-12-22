﻿"""_6743.py

AdditionalAccelerationOptions
"""


from mastapy._internal import constructor, conversion
from mastapy._math.vector_3d import Vector3D
from mastapy.utility import _1554
from mastapy._internal.python_net import python_net_import

_ADDITIONAL_ACCELERATION_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AdditionalAccelerationOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('AdditionalAccelerationOptions',)


class AdditionalAccelerationOptions(_1554.IndependentReportablePropertiesBase['AdditionalAccelerationOptions']):
    """AdditionalAccelerationOptions

    This is a mastapy class.
    """

    TYPE = _ADDITIONAL_ACCELERATION_OPTIONS

    def __init__(self, instance_to_wrap: 'AdditionalAccelerationOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_additional_acceleration(self) -> 'bool':
        """bool: 'IncludeAdditionalAcceleration' is the original name of this property."""

        temp = self.wrapped.IncludeAdditionalAcceleration

        if temp is None:
            return False

        return temp

    @include_additional_acceleration.setter
    def include_additional_acceleration(self, value: 'bool'):
        self.wrapped.IncludeAdditionalAcceleration = bool(value) if value is not None else False

    @property
    def magnitude(self) -> 'float':
        """float: 'Magnitude' is the original name of this property."""

        temp = self.wrapped.Magnitude

        if temp is None:
            return 0.0

        return temp

    @magnitude.setter
    def magnitude(self, value: 'float'):
        self.wrapped.Magnitude = float(value) if value is not None else 0.0

    @property
    def specify_direction_and_magnitude(self) -> 'bool':
        """bool: 'SpecifyDirectionAndMagnitude' is the original name of this property."""

        temp = self.wrapped.SpecifyDirectionAndMagnitude

        if temp is None:
            return False

        return temp

    @specify_direction_and_magnitude.setter
    def specify_direction_and_magnitude(self, value: 'bool'):
        self.wrapped.SpecifyDirectionAndMagnitude = bool(value) if value is not None else False

    @property
    def acceleration_vector(self) -> 'Vector3D':
        """Vector3D: 'AccelerationVector' is the original name of this property."""

        temp = self.wrapped.AccelerationVector

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @acceleration_vector.setter
    def acceleration_vector(self, value: 'Vector3D'):
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.AccelerationVector = value

    @property
    def orientation(self) -> 'Vector3D':
        """Vector3D: 'Orientation' is the original name of this property."""

        temp = self.wrapped.Orientation

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)
        return value

    @orientation.setter
    def orientation(self, value: 'Vector3D'):
        value = conversion.mp_to_pn_vector3d(value)
        self.wrapped.Orientation = value
