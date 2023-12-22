﻿"""_3840.py

WormGearMeshStabilityAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2288
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6915
from mastapy.system_model.analyses_and_results.stability_analyses import _3773
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'WormGearMeshStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshStabilityAnalysis',)


class WormGearMeshStabilityAnalysis(_3773.GearMeshStabilityAnalysis):
    """WormGearMeshStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MESH_STABILITY_ANALYSIS

    def __init__(self, instance_to_wrap: 'WormGearMeshStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2288.WormGearMesh':
        """WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6915.WormGearMeshLoadCase':
        """WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
