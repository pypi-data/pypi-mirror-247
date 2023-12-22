﻿"""_5791.py

DatapointForResponseOfANodeAtAFrequencyOnAHarmonic
"""


from typing import Optional

from mastapy._internal import constructor, conversion
from mastapy.math_utility import _1471, _1486
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DATAPOINT_FOR_RESPONSE_OF_A_NODE_AT_A_FREQUENCY_ON_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'DatapointForResponseOfANodeAtAFrequencyOnAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('DatapointForResponseOfANodeAtAFrequencyOnAHarmonic',)


class DatapointForResponseOfANodeAtAFrequencyOnAHarmonic(_0.APIBase):
    """DatapointForResponseOfANodeAtAFrequencyOnAHarmonic

    This is a mastapy class.
    """

    TYPE = _DATAPOINT_FOR_RESPONSE_OF_A_NODE_AT_A_FREQUENCY_ON_A_HARMONIC

    def __init__(self, instance_to_wrap: 'DatapointForResponseOfANodeAtAFrequencyOnAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_magnitude(self) -> 'float':
        """float: 'AngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularMagnitude

        if temp is None:
            return 0.0

        return temp

    @property
    def angular_radial_magnitude(self) -> 'float':
        """float: 'AngularRadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularRadialMagnitude

        if temp is None:
            return 0.0

        return temp

    @property
    def frequency(self) -> 'float':
        """float: 'Frequency' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Frequency

        if temp is None:
            return 0.0

        return temp

    @property
    def linear_magnitude(self) -> 'float':
        """float: 'LinearMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearMagnitude

        if temp is None:
            return 0.0

        return temp

    @property
    def radial_magnitude(self) -> 'float':
        """float: 'RadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialMagnitude

        if temp is None:
            return 0.0

        return temp

    @property
    def speed(self) -> 'float':
        """float: 'Speed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Speed

        if temp is None:
            return 0.0

        return temp

    @property
    def theta_x(self) -> 'complex':
        """complex: 'ThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThetaX

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)
        return value

    @property
    def theta_y(self) -> 'complex':
        """complex: 'ThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThetaY

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)
        return value

    @property
    def theta_z(self) -> 'complex':
        """complex: 'ThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThetaZ

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)
        return value

    @property
    def x(self) -> 'complex':
        """complex: 'X' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.X

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)
        return value

    @property
    def y(self) -> 'complex':
        """complex: 'Y' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Y

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)
        return value

    @property
    def z(self) -> 'complex':
        """complex: 'Z' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Z

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)
        return value

    def get_scalar_result(self, scalar_result: '_1471.DynamicsResponseScalarResult', complex_magnitude_method: Optional['_1486.ComplexMagnitudeMethod'] = _1486.ComplexMagnitudeMethod.PEAK_AMPLITUDE) -> 'complex':
        """ 'GetScalarResult' is the original name of this method.

        Args:
            scalar_result (mastapy.math_utility.DynamicsResponseScalarResult)
            complex_magnitude_method (mastapy.math_utility.ComplexMagnitudeMethod, optional)

        Returns:
            complex
        """

        scalar_result = conversion.mp_to_pn_enum(scalar_result)
        complex_magnitude_method = conversion.mp_to_pn_enum(complex_magnitude_method)
        return conversion.pn_to_mp_complex(self.wrapped.GetScalarResult(scalar_result, complex_magnitude_method))
