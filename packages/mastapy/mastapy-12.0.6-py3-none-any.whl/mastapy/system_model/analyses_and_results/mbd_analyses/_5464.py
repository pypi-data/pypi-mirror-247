﻿"""_5464.py

ZerolBevelGearSetMultibodyDynamicsAnalysis
"""


from typing import List

from mastapy.system_model.part_model.gears import _2510
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6919
from mastapy.system_model.analyses_and_results.mbd_analyses import _5463, _5462, _5339
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'ZerolBevelGearSetMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetMultibodyDynamicsAnalysis',)


class ZerolBevelGearSetMultibodyDynamicsAnalysis(_5339.BevelGearSetMultibodyDynamicsAnalysis):
    """ZerolBevelGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _ZEROL_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2510.ZerolBevelGearSet':
        """ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6919.ZerolBevelGearSetLoadCase':
        """ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears(self) -> 'List[_5463.ZerolBevelGearMultibodyDynamicsAnalysis]':
        """List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_gears_multibody_dynamics_analysis(self) -> 'List[_5463.ZerolBevelGearMultibodyDynamicsAnalysis]':
        """List[ZerolBevelGearMultibodyDynamicsAnalysis]: 'ZerolBevelGearsMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelGearsMultibodyDynamicsAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def zerol_bevel_meshes_multibody_dynamics_analysis(self) -> 'List[_5462.ZerolBevelGearMeshMultibodyDynamicsAnalysis]':
        """List[ZerolBevelGearMeshMultibodyDynamicsAnalysis]: 'ZerolBevelMeshesMultibodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ZerolBevelMeshesMultibodyDynamicsAnalysis

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
