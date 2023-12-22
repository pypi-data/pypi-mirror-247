﻿"""_2418.py

LoadSharingSettings
"""


from mastapy.system_model.part_model import _2417, _2395
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_LOAD_SHARING_SETTINGS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'LoadSharingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadSharingSettings',)


class LoadSharingSettings(_0.APIBase):
    """LoadSharingSettings

    This is a mastapy class.
    """

    TYPE = _LOAD_SHARING_SETTINGS

    def __init__(self, instance_to_wrap: 'LoadSharingSettings.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetary_load_sharing(self) -> '_2417.LoadSharingModes':
        """LoadSharingModes: 'PlanetaryLoadSharing' is the original name of this property."""

        temp = self.wrapped.PlanetaryLoadSharing

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2417.LoadSharingModes)(value) if value is not None else None

    @planetary_load_sharing.setter
    def planetary_load_sharing(self, value: '_2417.LoadSharingModes'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryLoadSharing = value

    @property
    def planetary_load_sharing_agma_application_level(self) -> '_2395.AGMALoadSharingTableApplicationLevel':
        """AGMALoadSharingTableApplicationLevel: 'PlanetaryLoadSharingAGMAApplicationLevel' is the original name of this property."""

        temp = self.wrapped.PlanetaryLoadSharingAGMAApplicationLevel

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_2395.AGMALoadSharingTableApplicationLevel)(value) if value is not None else None

    @planetary_load_sharing_agma_application_level.setter
    def planetary_load_sharing_agma_application_level(self, value: '_2395.AGMALoadSharingTableApplicationLevel'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.PlanetaryLoadSharingAGMAApplicationLevel = value
