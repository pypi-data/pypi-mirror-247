﻿"""_647.py

RealPlungeShaverOutputs
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _638, _644
from mastapy.gears.manufacturing.cylindrical import _606
from mastapy.gears.manufacturing.cylindrical.cutters import _703
from mastapy._internal.python_net import python_net_import

_REAL_PLUNGE_SHAVER_OUTPUTS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'RealPlungeShaverOutputs')


__docformat__ = 'restructuredtext en'
__all__ = ('RealPlungeShaverOutputs',)


class RealPlungeShaverOutputs(_644.PlungeShaverOutputs):
    """RealPlungeShaverOutputs

    This is a mastapy class.
    """

    TYPE = _REAL_PLUNGE_SHAVER_OUTPUTS

    def __init__(self, instance_to_wrap: 'RealPlungeShaverOutputs.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def face_width(self) -> 'float':
        """float: 'FaceWidth' is the original name of this property."""

        temp = self.wrapped.FaceWidth

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    def face_width(self, value: 'float'):
        self.wrapped.FaceWidth = float(value) if value is not None else 0.0

    @property
    def highest_shaver_tip_diameter(self) -> 'float':
        """float: 'HighestShaverTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HighestShaverTipDiameter

        if temp is None:
            return 0.0

        return temp

    @property
    def lead_measurement_method(self) -> '_638.MicroGeometryDefinitionMethod':
        """MicroGeometryDefinitionMethod: 'LeadMeasurementMethod' is the original name of this property."""

        temp = self.wrapped.LeadMeasurementMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_638.MicroGeometryDefinitionMethod)(value) if value is not None else None

    @lead_measurement_method.setter
    def lead_measurement_method(self, value: '_638.MicroGeometryDefinitionMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.LeadMeasurementMethod = value

    @property
    def lowest_shaver_tip_diameter(self) -> 'float':
        """float: 'LowestShaverTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LowestShaverTipDiameter

        if temp is None:
            return 0.0

        return temp

    @property
    def profile_measurement_method(self) -> '_638.MicroGeometryDefinitionMethod':
        """MicroGeometryDefinitionMethod: 'ProfileMeasurementMethod' is the original name of this property."""

        temp = self.wrapped.ProfileMeasurementMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_638.MicroGeometryDefinitionMethod)(value) if value is not None else None

    @profile_measurement_method.setter
    def profile_measurement_method(self, value: '_638.MicroGeometryDefinitionMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileMeasurementMethod = value

    @property
    def specify_face_width(self) -> 'bool':
        """bool: 'SpecifyFaceWidth' is the original name of this property."""

        temp = self.wrapped.SpecifyFaceWidth

        if temp is None:
            return False

        return temp

    @specify_face_width.setter
    def specify_face_width(self, value: 'bool'):
        self.wrapped.SpecifyFaceWidth = bool(value) if value is not None else False

    @property
    def left_flank_micro_geometry(self) -> '_606.CylindricalGearSpecifiedMicroGeometry':
        """CylindricalGearSpecifiedMicroGeometry: 'LeftFlankMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlankMicroGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank_micro_geometry(self) -> '_606.CylindricalGearSpecifiedMicroGeometry':
        """CylindricalGearSpecifiedMicroGeometry: 'RightFlankMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlankMicroGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def shaver(self) -> '_703.CylindricalGearPlungeShaver':
        """CylindricalGearPlungeShaver: 'Shaver' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Shaver

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micro_geometry(self) -> 'List[_606.CylindricalGearSpecifiedMicroGeometry]':
        """List[CylindricalGearSpecifiedMicroGeometry]: 'MicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicroGeometry

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def calculate_micro_geometry(self):
        """ 'CalculateMicroGeometry' is the original name of this method."""

        self.wrapped.CalculateMicroGeometry()

    def face_width_requires_calculation(self):
        """ 'FaceWidthRequiresCalculation' is the original name of this method."""

        self.wrapped.FaceWidthRequiresCalculation()
