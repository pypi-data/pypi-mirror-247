﻿"""_700.py

CylindricalGearFormGrindingWheel
"""


from mastapy._internal import constructor
from mastapy.math_utility import _1501
from mastapy.gears.manufacturing.cylindrical.cutters import _706
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_FORM_GRINDING_WHEEL = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters', 'CylindricalGearFormGrindingWheel')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearFormGrindingWheel',)


class CylindricalGearFormGrindingWheel(_706.CylindricalGearRealCutterDesign):
    """CylindricalGearFormGrindingWheel

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_FORM_GRINDING_WHEEL

    def __init__(self, instance_to_wrap: 'CylindricalGearFormGrindingWheel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def has_tolerances(self) -> 'bool':
        """bool: 'HasTolerances' is the original name of this property."""

        temp = self.wrapped.HasTolerances

        if temp is None:
            return False

        return temp

    @has_tolerances.setter
    def has_tolerances(self, value: 'bool'):
        self.wrapped.HasTolerances = bool(value) if value is not None else False

    @property
    def radius(self) -> 'float':
        """float: 'Radius' is the original name of this property."""

        temp = self.wrapped.Radius

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value is not None else 0.0

    @property
    def right_hand_cutting_edge_shape(self) -> '_1501.Vector2DListAccessor':
        """Vector2DListAccessor: 'RightHandCuttingEdgeShape' is the original name of this property."""

        temp = self.wrapped.RightHandCuttingEdgeShape

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @right_hand_cutting_edge_shape.setter
    def right_hand_cutting_edge_shape(self, value: '_1501.Vector2DListAccessor'):
        self.wrapped.RightHandCuttingEdgeShape = value
