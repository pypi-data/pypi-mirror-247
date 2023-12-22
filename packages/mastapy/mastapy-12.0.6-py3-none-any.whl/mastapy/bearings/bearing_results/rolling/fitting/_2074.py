﻿"""_2074.py

InterferenceComponents
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_INTERFERENCE_COMPONENTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.Fitting', 'InterferenceComponents')


__docformat__ = 'restructuredtext en'
__all__ = ('InterferenceComponents',)


class InterferenceComponents(_0.APIBase):
    """InterferenceComponents

    This is a mastapy class.
    """

    TYPE = _INTERFERENCE_COMPONENTS

    def __init__(self, instance_to_wrap: 'InterferenceComponents.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return ''

        return temp

    @property
    def nominal_interfacial_interference(self) -> 'float':
        """float: 'NominalInterfacialInterference' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NominalInterfacialInterference

        if temp is None:
            return 0.0

        return temp

    @property
    def reduction_in_interference_from_centrifugal_effects(self) -> 'float':
        """float: 'ReductionInInterferenceFromCentrifugalEffects' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReductionInInterferenceFromCentrifugalEffects

        if temp is None:
            return 0.0

        return temp

    @property
    def total_interfacial_interference(self) -> 'float':
        """float: 'TotalInterfacialInterference' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalInterfacialInterference

        if temp is None:
            return 0.0

        return temp
