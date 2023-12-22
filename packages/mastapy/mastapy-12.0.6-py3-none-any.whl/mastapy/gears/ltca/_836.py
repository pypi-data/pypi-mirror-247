﻿"""_836.py

GearMeshLoadedContactLine
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.ltca import _837
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_LOADED_CONTACT_LINE = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearMeshLoadedContactLine')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshLoadedContactLine',)


class GearMeshLoadedContactLine(_0.APIBase):
    """GearMeshLoadedContactLine

    This is a mastapy class.
    """

    TYPE = _GEAR_MESH_LOADED_CONTACT_LINE

    def __init__(self, instance_to_wrap: 'GearMeshLoadedContactLine.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_line_index(self) -> 'int':
        """int: 'ContactLineIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactLineIndex

        if temp is None:
            return 0

        return temp

    @property
    def mesh_position_index(self) -> 'int':
        """int: 'MeshPositionIndex' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshPositionIndex

        if temp is None:
            return 0

        return temp

    @property
    def tooth_number_of_gear_a(self) -> 'int':
        """int: 'ToothNumberOfGearA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothNumberOfGearA

        if temp is None:
            return 0

        return temp

    @property
    def tooth_number_of_gear_b(self) -> 'int':
        """int: 'ToothNumberOfGearB' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothNumberOfGearB

        if temp is None:
            return 0

        return temp

    @property
    def loaded_contact_strip_end_points(self) -> 'List[_837.GearMeshLoadedContactPoint]':
        """List[GearMeshLoadedContactPoint]: 'LoadedContactStripEndPoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadedContactStripEndPoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
