﻿"""_4101.py

ToothPassingHarmonic
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TOOTH_PASSING_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ToothPassingHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothPassingHarmonic',)


class ToothPassingHarmonic(_0.APIBase):
    """ToothPassingHarmonic

    This is a mastapy class.
    """

    TYPE = _TOOTH_PASSING_HARMONIC

    def __init__(self, instance_to_wrap: 'ToothPassingHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def harmonic_name(self) -> 'str':
        """str: 'HarmonicName' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HarmonicName

        if temp is None:
            return ''

        return temp

    @property
    def order(self) -> 'float':
        """float: 'Order' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Order

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_passing_frequency_at_reference_speed(self) -> 'float':
        """float: 'ToothPassingFrequencyAtReferenceSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothPassingFrequencyAtReferenceSpeed

        if temp is None:
            return 0.0

        return temp
