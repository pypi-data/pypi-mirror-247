﻿"""_1366.py

ISO4156SplineJointDesign
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.splines import _1386
from mastapy._internal.python_net import python_net_import

_ISO4156_SPLINE_JOINT_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'ISO4156SplineJointDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO4156SplineJointDesign',)


class ISO4156SplineJointDesign(_1386.StandardSplineJointDesign):
    """ISO4156SplineJointDesign

    This is a mastapy class.
    """

    TYPE = _ISO4156_SPLINE_JOINT_DESIGN

    def __init__(self, instance_to_wrap: 'ISO4156SplineJointDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def form_clearance(self) -> 'float':
        """float: 'FormClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.FormClearance

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_effective_clearance(self) -> 'float':
        """float: 'MaximumEffectiveClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumEffectiveClearance

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_effective_clearance(self) -> 'float':
        """float: 'MinimumEffectiveClearance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumEffectiveClearance

        if temp is None:
            return 0.0

        return temp
