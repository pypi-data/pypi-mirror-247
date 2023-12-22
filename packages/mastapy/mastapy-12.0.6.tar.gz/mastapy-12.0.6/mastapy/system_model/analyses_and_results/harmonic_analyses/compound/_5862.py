﻿"""_5862.py

CylindricalGearMeshCompoundHarmonicAnalysis
"""


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2268
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5670
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5873
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'CylindricalGearMeshCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundHarmonicAnalysis',)


class CylindricalGearMeshCompoundHarmonicAnalysis(_5873.GearMeshCompoundHarmonicAnalysis):
    """CylindricalGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2268.CylindricalGearMesh':
        """CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2268.CylindricalGearMesh':
        """CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_5670.CylindricalGearMeshHarmonicAnalysis]':
        """List[CylindricalGearMeshHarmonicAnalysis]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundHarmonicAnalysis]':
        """List[CylindricalGearMeshCompoundHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_5670.CylindricalGearMeshHarmonicAnalysis]':
        """List[CylindricalGearMeshHarmonicAnalysis]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
