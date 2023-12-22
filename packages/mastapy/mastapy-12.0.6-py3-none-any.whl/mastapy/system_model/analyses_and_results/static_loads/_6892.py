﻿"""_6892.py

StraightBevelDiffGearMeshLoadCase
"""


from mastapy.system_model.connections_and_sockets.gears import _2284
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6761
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'StraightBevelDiffGearMeshLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshLoadCase',)


class StraightBevelDiffGearMeshLoadCase(_6761.BevelGearMeshLoadCase):
    """StraightBevelDiffGearMeshLoadCase

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_LOAD_CASE

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2284.StraightBevelDiffGearMesh':
        """StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
