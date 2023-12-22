﻿"""_4865.py

HypoidGearMeshModalAnalysisAtAStiffness
"""


from mastapy.system_model.connections_and_sockets.gears import _2274
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6838
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4806
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'HypoidGearMeshModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshModalAnalysisAtAStiffness',)


class HypoidGearMeshModalAnalysisAtAStiffness(_4806.AGMAGleasonConicalGearMeshModalAnalysisAtAStiffness):
    """HypoidGearMeshModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _HYPOID_GEAR_MESH_MODAL_ANALYSIS_AT_A_STIFFNESS

    def __init__(self, instance_to_wrap: 'HypoidGearMeshModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2274.HypoidGearMesh':
        """HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6838.HypoidGearMeshLoadCase':
        """HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
