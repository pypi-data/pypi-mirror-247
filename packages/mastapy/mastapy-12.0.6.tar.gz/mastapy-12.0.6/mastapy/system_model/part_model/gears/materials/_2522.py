﻿"""_2522.py

GearMaterialExpertSystemMaterialDetails
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_DETAILS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears.Materials', 'GearMaterialExpertSystemMaterialDetails')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMaterialExpertSystemMaterialDetails',)


class GearMaterialExpertSystemMaterialDetails(_0.APIBase):
    """GearMaterialExpertSystemMaterialDetails

    This is a mastapy class.
    """

    TYPE = _GEAR_MATERIAL_EXPERT_SYSTEM_MATERIAL_DETAILS

    def __init__(self, instance_to_wrap: 'GearMaterialExpertSystemMaterialDetails.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bar_length(self) -> 'float':
        """float: 'BarLength' is the original name of this property."""

        temp = self.wrapped.BarLength

        if temp is None:
            return 0.0

        return temp

    @bar_length.setter
    def bar_length(self, value: 'float'):
        self.wrapped.BarLength = float(value) if value is not None else 0.0
