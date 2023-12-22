﻿"""_441.py

FaceGearMeshRating
"""


from typing import List

from mastapy.gears import _320
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.face import _984
from mastapy.gears.rating.face import _444, _442
from mastapy.gears.load_case.face import _874
from mastapy.gears.rating.cylindrical.iso6336 import _507, _509
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating import _354
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Face', 'FaceGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshRating',)


class FaceGearMeshRating(_354.GearMeshRating):
    """FaceGearMeshRating

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'FaceGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_flank(self) -> '_320.GearFlanks':
        """GearFlanks: 'ActiveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ActiveFlank

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_320.GearFlanks)(value) if value is not None else None

    @property
    def face_gear_mesh(self) -> '_984.FaceGearMeshDesign':
        """FaceGearMeshDesign: 'FaceGearMesh' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearMesh

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gear_set_rating(self) -> '_444.FaceGearSetRating':
        """FaceGearSetRating: 'GearSetRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearSetRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_load_case(self) -> '_874.FaceMeshLoadCase':
        """FaceMeshLoadCase: 'MeshLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def mesh_single_flank_rating(self) -> '_507.ISO63362006MeshSingleFlankRating':
        """ISO63362006MeshSingleFlankRating: 'MeshSingleFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshSingleFlankRating

        if temp is None:
            return None

        if _507.ISO63362006MeshSingleFlankRating.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast mesh_single_flank_rating to ISO63362006MeshSingleFlankRating. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def face_gear_ratings(self) -> 'List[_442.FaceGearRating]':
        """List[FaceGearRating]: 'FaceGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FaceGearRatings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
