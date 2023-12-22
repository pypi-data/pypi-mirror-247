﻿"""_35.py

ShaftSafetyFactorSettings
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SHAFT_SAFETY_FACTOR_SETTINGS = python_net_import('SMT.MastaAPI.Shafts', 'ShaftSafetyFactorSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSafetyFactorSettings',)


class ShaftSafetyFactorSettings(_0.APIBase):
    """ShaftSafetyFactorSettings

    This is a mastapy class.
    """

    TYPE = _SHAFT_SAFETY_FACTOR_SETTINGS

    def __init__(self, instance_to_wrap: 'ShaftSafetyFactorSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def shaft_fatigue_safety_factor_requirement(self) -> 'float':
        """float: 'ShaftFatigueSafetyFactorRequirement' is the original name of this property."""

        temp = self.wrapped.ShaftFatigueSafetyFactorRequirement

        if temp is None:
            return 0.0

        return temp

    @shaft_fatigue_safety_factor_requirement.setter
    def shaft_fatigue_safety_factor_requirement(self, value: 'float'):
        self.wrapped.ShaftFatigueSafetyFactorRequirement = float(value) if value is not None else 0.0

    @property
    def shaft_static_safety_factor_requirement(self) -> 'float':
        """float: 'ShaftStaticSafetyFactorRequirement' is the original name of this property."""

        temp = self.wrapped.ShaftStaticSafetyFactorRequirement

        if temp is None:
            return 0.0

        return temp

    @shaft_static_safety_factor_requirement.setter
    def shaft_static_safety_factor_requirement(self, value: 'float'):
        self.wrapped.ShaftStaticSafetyFactorRequirement = float(value) if value is not None else 0.0
