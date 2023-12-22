﻿"""_2286.py

StraightBevelGearMesh
"""


from mastapy.gears.gear_designs.straight_bevel import _955
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets.gears import _2262
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMesh',)


class StraightBevelGearMesh(_2262.BevelGearMesh):
    """StraightBevelGearMesh

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_GEAR_MESH

    def __init__(self, instance_to_wrap: 'StraightBevelGearMesh.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bevel_gear_mesh_design(self) -> '_955.StraightBevelGearMeshDesign':
        """StraightBevelGearMeshDesign: 'BevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BevelGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def straight_bevel_gear_mesh_design(self) -> '_955.StraightBevelGearMeshDesign':
        """StraightBevelGearMeshDesign: 'StraightBevelGearMeshDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StraightBevelGearMeshDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
