﻿"""_775.py

ConicalMeshFlankMicroGeometryConfig
"""


from mastapy._internal import constructor
from mastapy.gears.gear_designs.conical.micro_geometry import _1163
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_FLANK_MICRO_GEOMETRY_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshFlankMicroGeometryConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshFlankMicroGeometryConfig',)


class ConicalMeshFlankMicroGeometryConfig(_0.APIBase):
    """ConicalMeshFlankMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESH_FLANK_MICRO_GEOMETRY_CONFIG

    def __init__(self, instance_to_wrap: 'ConicalMeshFlankMicroGeometryConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def delta_h_as_percent_of_face_width(self) -> 'float':
        """float: 'DeltaHAsPercentOfFaceWidth' is the original name of this property."""

        temp = self.wrapped.DeltaHAsPercentOfFaceWidth

        if temp is None:
            return 0.0

        return temp

    @delta_h_as_percent_of_face_width.setter
    def delta_h_as_percent_of_face_width(self, value: 'float'):
        self.wrapped.DeltaHAsPercentOfFaceWidth = float(value) if value is not None else 0.0

    @property
    def delta_v_as_percent_of_wheel_tip_to_fillet_flank_boundary(self) -> 'float':
        """float: 'DeltaVAsPercentOfWheelTipToFilletFlankBoundary' is the original name of this property."""

        temp = self.wrapped.DeltaVAsPercentOfWheelTipToFilletFlankBoundary

        if temp is None:
            return 0.0

        return temp

    @delta_v_as_percent_of_wheel_tip_to_fillet_flank_boundary.setter
    def delta_v_as_percent_of_wheel_tip_to_fillet_flank_boundary(self, value: 'float'):
        self.wrapped.DeltaVAsPercentOfWheelTipToFilletFlankBoundary = float(value) if value is not None else 0.0

    @property
    def perform_vh_check(self) -> 'bool':
        """bool: 'PerformVHCheck' is the original name of this property."""

        temp = self.wrapped.PerformVHCheck

        if temp is None:
            return False

        return temp

    @perform_vh_check.setter
    def perform_vh_check(self, value: 'bool'):
        self.wrapped.PerformVHCheck = bool(value) if value is not None else False

    @property
    def specified_ease_off_surface(self) -> '_1163.ConicalGearFlankMicroGeometry':
        """ConicalGearFlankMicroGeometry: 'SpecifiedEaseOffSurface' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SpecifiedEaseOffSurface

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
