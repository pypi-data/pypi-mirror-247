﻿"""_2523.py

GearMaterialExpertSystemMaterialOptions
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.Materials', 'GearMaterialExpertSystemMaterialOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMaterialExpertSystemMaterialOptions',)


class GearMaterialExpertSystemMaterialOptions(_0.APIBase):
    """GearMaterialExpertSystemMaterialOptions

    This is a mastapy class.
    """

    TYPE = _GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_OPTIONS

    def __init__(self, instance_to_wrap: 'GearMaterialExpertSystemMaterialOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def maximum_damage(self) -> 'float':
        """float: 'MaximumDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumDamage

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_safety_factor(self) -> 'float':
        """float: 'MaximumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumSafetyFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_damage(self) -> 'float':
        """float: 'MinimumDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumDamage

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_safety_factor(self) -> 'float':
        """float: 'MinimumSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumSafetyFactor

        if temp is None:
            return 0.0

        return temp
