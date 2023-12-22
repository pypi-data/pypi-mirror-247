﻿"""_5460.py

WormGearMultibodyDynamicsAnalysis
"""


from mastapy.system_model.part_model.gears import _2507
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6914
from mastapy.system_model.analyses_and_results.mbd_analyses import _5382
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'WormGearMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMultibodyDynamicsAnalysis',)


class WormGearMultibodyDynamicsAnalysis(_5382.GearMultibodyDynamicsAnalysis):
    """WormGearMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _WORM_GEAR_MULTIBODY_DYNAMICS_ANALYSIS

    def __init__(self, instance_to_wrap: 'WormGearMultibodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2507.WormGear':
        """WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6914.WormGearLoadCase':
        """WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
