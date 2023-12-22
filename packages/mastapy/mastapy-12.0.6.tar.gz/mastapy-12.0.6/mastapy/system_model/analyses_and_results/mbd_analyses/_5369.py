﻿"""_5369.py

CylindricalGearMeshMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.connections_and_sockets.gears import _2268
from mastapy.system_model.analyses_and_results.static_loads import _6795
from mastapy.system_model.analyses_and_results.mbd_analyses import _5380
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CylindricalGearMeshMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshMultibodyDynamicsAnalysis',)


class CylindricalGearMeshMultibodyDynamicsAnalysis(_5380.GearMeshMultibodyDynamicsAnalysis):
    """CylindricalGearMeshMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_stress_gear_a_left_flank(self) -> 'float':
        """float: 'ContactStressGearALeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressGearALeftFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_stress_gear_a_right_flank(self) -> 'float':
        """float: 'ContactStressGearARightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressGearARightFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_stress_gear_b_left_flank(self) -> 'float':
        """float: 'ContactStressGearBLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressGearBLeftFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_stress_gear_b_right_flank(self) -> 'float':
        """float: 'ContactStressGearBRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStressGearBRightFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_root_stress_gear_a_left_flank(self) -> 'float':
        """float: 'ToothRootStressGearALeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootStressGearALeftFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_root_stress_gear_a_right_flank(self) -> 'float':
        """float: 'ToothRootStressGearARightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootStressGearARightFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_root_stress_gear_b_left_flank(self) -> 'float':
        """float: 'ToothRootStressGearBLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootStressGearBLeftFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def tooth_root_stress_gear_b_right_flank(self) -> 'float':
        """float: 'ToothRootStressGearBRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ToothRootStressGearBRightFlank

        if temp is None:
            return 0.0

        return temp

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
    def planetaries(self) -> 'List[CylindricalGearMeshMultibodyDynamicsAnalysis]':
        """List[CylindricalGearMeshMultibodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
