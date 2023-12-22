﻿"""_5718.py

KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis
"""


from mastapy.system_model.connections_and_sockets.gears import _2279
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6851
from mastapy.system_model.analyses_and_results.system_deflections import _2725
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5712
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis(_5712.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis):
    """KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2279.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        """KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_load_case(self) -> '_6851.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase':
        """KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2725.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        """KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
