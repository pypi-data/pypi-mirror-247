﻿"""_7048.py

StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation
"""


from mastapy.system_model.connections_and_sockets.gears import _2284
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6892
from mastapy.system_model.analyses_and_results.system_deflections import _2764
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6958
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation',)


class StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation(_6958.BevelGearMeshAdvancedTimeSteppingAnalysisForModulation):
    """StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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

    @property
    def connection_load_case(self) -> '_6892.StraightBevelDiffGearMeshLoadCase':
        """StraightBevelDiffGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2764.StraightBevelDiffGearMeshSystemDeflection':
        """StraightBevelDiffGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
