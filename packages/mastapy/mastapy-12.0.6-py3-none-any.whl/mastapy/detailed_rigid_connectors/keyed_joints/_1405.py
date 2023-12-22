﻿"""_1405.py

KeywayJointHalfDesign
"""


from mastapy._internal import constructor
from mastapy.detailed_rigid_connectors.interference_fits import _1412
from mastapy._internal.python_net import python_net_import

_KEYWAY_JOINT_HALF_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints', 'KeywayJointHalfDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KeywayJointHalfDesign',)


class KeywayJointHalfDesign(_1412.InterferenceFitHalfDesign):
    """KeywayJointHalfDesign

    This is a mastapy class.
    """

    TYPE = _KEYWAY_JOINT_HALF_DESIGN

    def __init__(self, instance_to_wrap: 'KeywayJointHalfDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def effective_keyway_depth(self) -> 'float':
        """float: 'EffectiveKeywayDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveKeywayDepth

        if temp is None:
            return 0.0

        return temp

    @property
    def hardness_factor(self) -> 'float':
        """float: 'HardnessFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HardnessFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def is_case_hardened(self) -> 'bool':
        """bool: 'IsCaseHardened' is the original name of this property."""

        temp = self.wrapped.IsCaseHardened

        if temp is None:
            return False

        return temp

    @is_case_hardened.setter
    def is_case_hardened(self, value: 'bool'):
        self.wrapped.IsCaseHardened = bool(value) if value is not None else False

    @property
    def keyway_chamfer_depth(self) -> 'float':
        """float: 'KeywayChamferDepth' is the original name of this property."""

        temp = self.wrapped.KeywayChamferDepth

        if temp is None:
            return 0.0

        return temp

    @keyway_chamfer_depth.setter
    def keyway_chamfer_depth(self, value: 'float'):
        self.wrapped.KeywayChamferDepth = float(value) if value is not None else 0.0

    @property
    def name(self) -> 'str':
        """str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Name

        if temp is None:
            return ''

        return temp

    @property
    def support_factor(self) -> 'float':
        """float: 'SupportFactor' is the original name of this property."""

        temp = self.wrapped.SupportFactor

        if temp is None:
            return 0.0

        return temp

    @support_factor.setter
    def support_factor(self, value: 'float'):
        self.wrapped.SupportFactor = float(value) if value is not None else 0.0
