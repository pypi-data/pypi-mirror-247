﻿"""_4000.py

BoltedJointPowerFlow
"""


from mastapy.system_model.part_model import _2400
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6763
from mastapy.system_model.analyses_and_results.power_flows import _4082
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'BoltedJointPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointPowerFlow',)


class BoltedJointPowerFlow(_4082.SpecialisedAssemblyPowerFlow):
    """BoltedJointPowerFlow

    This is a mastapy class.
    """

    TYPE = _BOLTED_JOINT_POWER_FLOW

    def __init__(self, instance_to_wrap: 'BoltedJointPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2400.BoltedJoint':
        """BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6763.BoltedJointLoadCase':
        """BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
