﻿"""_6763.py

BoltedJointLoadCase
"""


from mastapy.system_model.part_model import _2400
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6884
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'BoltedJointLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointLoadCase',)


class BoltedJointLoadCase(_6884.SpecialisedAssemblyLoadCase):
    """BoltedJointLoadCase

    This is a mastapy class.
    """

    TYPE = _BOLTED_JOINT_LOAD_CASE

    def __init__(self, instance_to_wrap: 'BoltedJointLoadCase.TYPE'):
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
