﻿"""_1403.py

KeyedJointDesign
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.detailed_rigid_connectors.keyed_joints import _1404, _1406
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.detailed_rigid_connectors.interference_fits import _1411
from mastapy._internal.python_net import python_net_import

_KEYED_JOINT_DESIGN = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints', 'KeyedJointDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('KeyedJointDesign',)


class KeyedJointDesign(_1411.InterferenceFitDesign):
    """KeyedJointDesign

    This is a mastapy class.
    """

    TYPE = _KEYED_JOINT_DESIGN

    def __init__(self, instance_to_wrap: 'KeyedJointDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def allowable_contact_stress_for_inner_component(self) -> 'float':
        """float: 'AllowableContactStressForInnerComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableContactStressForInnerComponent

        if temp is None:
            return 0.0

        return temp

    @property
    def allowable_contact_stress_for_key(self) -> 'float':
        """float: 'AllowableContactStressForKey' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableContactStressForKey

        if temp is None:
            return 0.0

        return temp

    @property
    def allowable_contact_stress_for_outer_component(self) -> 'float':
        """float: 'AllowableContactStressForOuterComponent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AllowableContactStressForOuterComponent

        if temp is None:
            return 0.0

        return temp

    @property
    def edge_chamfer(self) -> 'float':
        """float: 'EdgeChamfer' is the original name of this property."""

        temp = self.wrapped.EdgeChamfer

        if temp is None:
            return 0.0

        return temp

    @edge_chamfer.setter
    def edge_chamfer(self, value: 'float'):
        self.wrapped.EdgeChamfer = float(value) if value is not None else 0.0

    @property
    def geometry_type(self) -> '_1404.KeyTypes':
        """KeyTypes: 'GeometryType' is the original name of this property."""

        temp = self.wrapped.GeometryType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1404.KeyTypes)(value) if value is not None else None

    @geometry_type.setter
    def geometry_type(self, value: '_1404.KeyTypes'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GeometryType = value

    @property
    def height(self) -> 'float':
        """float: 'Height' is the original name of this property."""

        temp = self.wrapped.Height

        if temp is None:
            return 0.0

        return temp

    @height.setter
    def height(self, value: 'float'):
        self.wrapped.Height = float(value) if value is not None else 0.0

    @property
    def inclined_underside_chamfer(self) -> 'float':
        """float: 'InclinedUndersideChamfer' is the original name of this property."""

        temp = self.wrapped.InclinedUndersideChamfer

        if temp is None:
            return 0.0

        return temp

    @inclined_underside_chamfer.setter
    def inclined_underside_chamfer(self, value: 'float'):
        self.wrapped.InclinedUndersideChamfer = float(value) if value is not None else 0.0

    @property
    def interference_fit_length(self) -> 'float':
        """float: 'InterferenceFitLength' is the original name of this property."""

        temp = self.wrapped.InterferenceFitLength

        if temp is None:
            return 0.0

        return temp

    @interference_fit_length.setter
    def interference_fit_length(self, value: 'float'):
        self.wrapped.InterferenceFitLength = float(value) if value is not None else 0.0

    @property
    def is_interference_fit(self) -> 'bool':
        """bool: 'IsInterferenceFit' is the original name of this property."""

        temp = self.wrapped.IsInterferenceFit

        if temp is None:
            return False

        return temp

    @is_interference_fit.setter
    def is_interference_fit(self, value: 'bool'):
        self.wrapped.IsInterferenceFit = bool(value) if value is not None else False

    @property
    def is_key_case_hardened(self) -> 'bool':
        """bool: 'IsKeyCaseHardened' is the original name of this property."""

        temp = self.wrapped.IsKeyCaseHardened

        if temp is None:
            return False

        return temp

    @is_key_case_hardened.setter
    def is_key_case_hardened(self, value: 'bool'):
        self.wrapped.IsKeyCaseHardened = bool(value) if value is not None else False

    @property
    def key_effective_length(self) -> 'float':
        """float: 'KeyEffectiveLength' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.KeyEffectiveLength

        if temp is None:
            return 0.0

        return temp

    @property
    def keyway_depth_inner_component(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'KeywayDepthInnerComponent' is the original name of this property."""

        temp = self.wrapped.KeywayDepthInnerComponent

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @keyway_depth_inner_component.setter
    def keyway_depth_inner_component(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.KeywayDepthInnerComponent = value

    @property
    def keyway_depth_outer_component(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'KeywayDepthOuterComponent' is the original name of this property."""

        temp = self.wrapped.KeywayDepthOuterComponent

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @keyway_depth_outer_component.setter
    def keyway_depth_outer_component(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.KeywayDepthOuterComponent = value

    @property
    def length(self) -> 'float':
        """float: 'Length' is the original name of this property."""

        temp = self.wrapped.Length

        if temp is None:
            return 0.0

        return temp

    @length.setter
    def length(self, value: 'float'):
        self.wrapped.Length = float(value) if value is not None else 0.0

    @property
    def number_of_keys(self) -> '_1406.NumberOfKeys':
        """NumberOfKeys: 'NumberOfKeys' is the original name of this property."""

        temp = self.wrapped.NumberOfKeys

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1406.NumberOfKeys)(value) if value is not None else None

    @number_of_keys.setter
    def number_of_keys(self, value: '_1406.NumberOfKeys'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.NumberOfKeys = value

    @property
    def position_offset(self) -> 'float':
        """float: 'PositionOffset' is the original name of this property."""

        temp = self.wrapped.PositionOffset

        if temp is None:
            return 0.0

        return temp

    @position_offset.setter
    def position_offset(self, value: 'float'):
        self.wrapped.PositionOffset = float(value) if value is not None else 0.0

    @property
    def tensile_yield_strength(self) -> 'float':
        """float: 'TensileYieldStrength' is the original name of this property."""

        temp = self.wrapped.TensileYieldStrength

        if temp is None:
            return 0.0

        return temp

    @tensile_yield_strength.setter
    def tensile_yield_strength(self, value: 'float'):
        self.wrapped.TensileYieldStrength = float(value) if value is not None else 0.0

    @property
    def width(self) -> 'float':
        """float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return 0.0

        return temp

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value is not None else 0.0
