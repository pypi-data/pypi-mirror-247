﻿"""_6779.py

ConicalGearSetHarmonicLoadData
"""


from typing import List

from mastapy.gears import _343
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.math_utility import _1479
from mastapy.system_model.analyses_and_results.static_loads import _6826
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET_HARMONIC_LOAD_DATA = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ConicalGearSetHarmonicLoadData')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearSetHarmonicLoadData',)


class ConicalGearSetHarmonicLoadData(_6826.GearSetHarmonicLoadData):
    """ConicalGearSetHarmonicLoadData

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_SET_HARMONIC_LOAD_DATA

    def __init__(self, instance_to_wrap: 'ConicalGearSetHarmonicLoadData.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def te_specification_type(self) -> '_343.TESpecificationType':
        """TESpecificationType: 'TESpecificationType' is the original name of this property."""

        temp = self.wrapped.TESpecificationType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_343.TESpecificationType)(value) if value is not None else None

    @te_specification_type.setter
    def te_specification_type(self, value: '_343.TESpecificationType'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TESpecificationType = value

    @property
    def excitations(self) -> 'List[_1479.FourierSeries]':
        """List[FourierSeries]: 'Excitations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Excitations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def read_data_from_gleason_gemsxml(self):
        """ 'ReadDataFromGleasonGEMSXML' is the original name of this method."""

        self.wrapped.ReadDataFromGleasonGEMSXML()

    def read_data_from_ki_mo_sxml(self):
        """ 'ReadDataFromKIMoSXML' is the original name of this method."""

        self.wrapped.ReadDataFromKIMoSXML()
