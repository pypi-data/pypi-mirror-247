﻿"""_4290.py

CylindricalGearMeshParametricStudyTool
"""


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _2268
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6795
from mastapy.system_model.analyses_and_results.system_deflections import _2690
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4308
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CylindricalGearMeshParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshParametricStudyTool',)


class CylindricalGearMeshParametricStudyTool(_4308.GearMeshParametricStudyTool):
    """CylindricalGearMeshParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def connection_load_case(self) -> '_6795.CylindricalGearMeshLoadCase':
        """CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2690.CylindricalGearMeshSystemDeflection]':
        """List[CylindricalGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionSystemDeflectionResults

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshParametricStudyTool]':
        """List[CylindricalGearMeshParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
