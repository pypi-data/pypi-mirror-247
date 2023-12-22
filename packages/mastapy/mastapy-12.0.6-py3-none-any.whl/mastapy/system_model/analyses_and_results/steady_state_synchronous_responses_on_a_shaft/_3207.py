﻿"""_3207.py

BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft
"""


from mastapy.system_model.connections_and_sockets.gears import _2260
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6756
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3212
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft',)


class BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft(_3212.BevelGearMeshSteadyStateSynchronousResponseOnAShaft):
    """BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2260.BevelDifferentialGearMesh':
        """BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6756.BevelDifferentialGearMeshLoadCase':
        """BevelDifferentialGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
