﻿"""_1088.py

CylindricalGearLeadModification
"""


from typing import Optional

from mastapy._internal import constructor
from mastapy.utility_gui.charts import (
    _1830, _1816, _1823, _1825
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.micro_geometry import _565
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_LEAD_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearLeadModification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearLeadModification',)


class CylindricalGearLeadModification(_565.LeadModification):
    """CylindricalGearLeadModification

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_LEAD_MODIFICATION

    def __init__(self, instance_to_wrap: 'CylindricalGearLeadModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def evaluation_left_limit(self) -> 'float':
        """float: 'EvaluationLeftLimit' is the original name of this property."""

        temp = self.wrapped.EvaluationLeftLimit

        if temp is None:
            return 0.0

        return temp

    @evaluation_left_limit.setter
    def evaluation_left_limit(self, value: 'float'):
        self.wrapped.EvaluationLeftLimit = float(value) if value is not None else 0.0

    @property
    def evaluation_of_linear_left_relief(self) -> 'float':
        """float: 'EvaluationOfLinearLeftRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearLeftRelief

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_left_relief.setter
    def evaluation_of_linear_left_relief(self, value: 'float'):
        self.wrapped.EvaluationOfLinearLeftRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_of_linear_right_relief(self) -> 'float':
        """float: 'EvaluationOfLinearRightRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearRightRelief

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_right_relief.setter
    def evaluation_of_linear_right_relief(self, value: 'float'):
        self.wrapped.EvaluationOfLinearRightRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_of_parabolic_left_relief(self) -> 'float':
        """float: 'EvaluationOfParabolicLeftRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicLeftRelief

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_left_relief.setter
    def evaluation_of_parabolic_left_relief(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicLeftRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_of_parabolic_right_relief(self) -> 'float':
        """float: 'EvaluationOfParabolicRightRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicRightRelief

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_right_relief.setter
    def evaluation_of_parabolic_right_relief(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicRightRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_right_limit(self) -> 'float':
        """float: 'EvaluationRightLimit' is the original name of this property."""

        temp = self.wrapped.EvaluationRightLimit

        if temp is None:
            return 0.0

        return temp

    @evaluation_right_limit.setter
    def evaluation_right_limit(self, value: 'float'):
        self.wrapped.EvaluationRightLimit = float(value) if value is not None else 0.0

    @property
    def evaluation_side_limit(self) -> 'Optional[float]':
        """Optional[float]: 'EvaluationSideLimit' is the original name of this property."""

        temp = self.wrapped.EvaluationSideLimit

        if temp is None:
            return None

        return temp

    @evaluation_side_limit.setter
    def evaluation_side_limit(self, value: 'Optional[float]'):
        self.wrapped.EvaluationSideLimit = value

    @property
    def evaluation_of_linear_side_relief(self) -> 'Optional[float]':
        """Optional[float]: 'EvaluationOfLinearSideRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearSideRelief

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_side_relief.setter
    def evaluation_of_linear_side_relief(self, value: 'Optional[float]'):
        self.wrapped.EvaluationOfLinearSideRelief = value

    @property
    def evaluation_of_parabolic_side_relief(self) -> 'Optional[float]':
        """Optional[float]: 'EvaluationOfParabolicSideRelief' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicSideRelief

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_side_relief.setter
    def evaluation_of_parabolic_side_relief(self, value: 'Optional[float]'):
        self.wrapped.EvaluationOfParabolicSideRelief = value

    @property
    def helix_angle_modification_at_original_reference_diameter(self) -> 'float':
        """float: 'HelixAngleModificationAtOriginalReferenceDiameter' is the original name of this property."""

        temp = self.wrapped.HelixAngleModificationAtOriginalReferenceDiameter

        if temp is None:
            return 0.0

        return temp

    @helix_angle_modification_at_original_reference_diameter.setter
    def helix_angle_modification_at_original_reference_diameter(self, value: 'float'):
        self.wrapped.HelixAngleModificationAtOriginalReferenceDiameter = float(value) if value is not None else 0.0

    @property
    def lead_modification_chart(self) -> '_1830.TwoDChartDefinition':
        """TwoDChartDefinition: 'LeadModificationChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeadModificationChart

        if temp is None:
            return None

        if _1830.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast lead_modification_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def linear_relief_isodinagmavdi(self) -> 'float':
        """float: 'LinearReliefISODINAGMAVDI' is the original name of this property."""

        temp = self.wrapped.LinearReliefISODINAGMAVDI

        if temp is None:
            return 0.0

        return temp

    @linear_relief_isodinagmavdi.setter
    def linear_relief_isodinagmavdi(self, value: 'float'):
        self.wrapped.LinearReliefISODINAGMAVDI = float(value) if value is not None else 0.0

    @property
    def linear_relief_isodinagmavdi_across_full_face_width(self) -> 'float':
        """float: 'LinearReliefISODINAGMAVDIAcrossFullFaceWidth' is the original name of this property."""

        temp = self.wrapped.LinearReliefISODINAGMAVDIAcrossFullFaceWidth

        if temp is None:
            return 0.0

        return temp

    @linear_relief_isodinagmavdi_across_full_face_width.setter
    def linear_relief_isodinagmavdi_across_full_face_width(self, value: 'float'):
        self.wrapped.LinearReliefISODINAGMAVDIAcrossFullFaceWidth = float(value) if value is not None else 0.0

    @property
    def linear_relief_ldp(self) -> 'float':
        """float: 'LinearReliefLDP' is the original name of this property."""

        temp = self.wrapped.LinearReliefLDP

        if temp is None:
            return 0.0

        return temp

    @linear_relief_ldp.setter
    def linear_relief_ldp(self, value: 'float'):
        self.wrapped.LinearReliefLDP = float(value) if value is not None else 0.0

    @property
    def linear_relief_ldp_across_full_face_width(self) -> 'float':
        """float: 'LinearReliefLDPAcrossFullFaceWidth' is the original name of this property."""

        temp = self.wrapped.LinearReliefLDPAcrossFullFaceWidth

        if temp is None:
            return 0.0

        return temp

    @linear_relief_ldp_across_full_face_width.setter
    def linear_relief_ldp_across_full_face_width(self, value: 'float'):
        self.wrapped.LinearReliefLDPAcrossFullFaceWidth = float(value) if value is not None else 0.0

    @property
    def linear_relief_across_full_face_width(self) -> 'float':
        """float: 'LinearReliefAcrossFullFaceWidth' is the original name of this property."""

        temp = self.wrapped.LinearReliefAcrossFullFaceWidth

        if temp is None:
            return 0.0

        return temp

    @linear_relief_across_full_face_width.setter
    def linear_relief_across_full_face_width(self, value: 'float'):
        self.wrapped.LinearReliefAcrossFullFaceWidth = float(value) if value is not None else 0.0

    @property
    def modified_base_helix_angle(self) -> 'float':
        """float: 'ModifiedBaseHelixAngle' is the original name of this property."""

        temp = self.wrapped.ModifiedBaseHelixAngle

        if temp is None:
            return 0.0

        return temp

    @modified_base_helix_angle.setter
    def modified_base_helix_angle(self, value: 'float'):
        self.wrapped.ModifiedBaseHelixAngle = float(value) if value is not None else 0.0

    @property
    def modified_helix_angle_assuming_unmodified_normal_module(self) -> 'float':
        """float: 'ModifiedHelixAngleAssumingUnmodifiedNormalModule' is the original name of this property."""

        temp = self.wrapped.ModifiedHelixAngleAssumingUnmodifiedNormalModule

        if temp is None:
            return 0.0

        return temp

    @modified_helix_angle_assuming_unmodified_normal_module.setter
    def modified_helix_angle_assuming_unmodified_normal_module(self, value: 'float'):
        self.wrapped.ModifiedHelixAngleAssumingUnmodifiedNormalModule = float(value) if value is not None else 0.0

    @property
    def modified_helix_angle_at_original_reference_diameter(self) -> 'float':
        """float: 'ModifiedHelixAngleAtOriginalReferenceDiameter' is the original name of this property."""

        temp = self.wrapped.ModifiedHelixAngleAtOriginalReferenceDiameter

        if temp is None:
            return 0.0

        return temp

    @modified_helix_angle_at_original_reference_diameter.setter
    def modified_helix_angle_at_original_reference_diameter(self, value: 'float'):
        self.wrapped.ModifiedHelixAngleAtOriginalReferenceDiameter = float(value) if value is not None else 0.0

    @property
    def modified_normal_pressure_angle_due_to_helix_angle_modification_assuming_unmodified_normal_module(self) -> 'float':
        """float: 'ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedNormalPressureAngleDueToHelixAngleModificationAssumingUnmodifiedNormalModule

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_normal_pressure_angle_due_to_helix_angle_modification_at_original_reference_diameter(self) -> 'float':
        """float: 'ModifiedNormalPressureAngleDueToHelixAngleModificationAtOriginalReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedNormalPressureAngleDueToHelixAngleModificationAtOriginalReferenceDiameter

        if temp is None:
            return 0.0

        return temp

    @property
    def start_of_linear_left_relief(self) -> 'float':
        """float: 'StartOfLinearLeftRelief' is the original name of this property."""

        temp = self.wrapped.StartOfLinearLeftRelief

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_left_relief.setter
    def start_of_linear_left_relief(self, value: 'float'):
        self.wrapped.StartOfLinearLeftRelief = float(value) if value is not None else 0.0

    @property
    def start_of_linear_right_relief(self) -> 'float':
        """float: 'StartOfLinearRightRelief' is the original name of this property."""

        temp = self.wrapped.StartOfLinearRightRelief

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_right_relief.setter
    def start_of_linear_right_relief(self, value: 'float'):
        self.wrapped.StartOfLinearRightRelief = float(value) if value is not None else 0.0

    @property
    def start_of_linear_side_relief(self) -> 'Optional[float]':
        """Optional[float]: 'StartOfLinearSideRelief' is the original name of this property."""

        temp = self.wrapped.StartOfLinearSideRelief

        if temp is None:
            return None

        return temp

    @start_of_linear_side_relief.setter
    def start_of_linear_side_relief(self, value: 'Optional[float]'):
        self.wrapped.StartOfLinearSideRelief = value

    @property
    def start_of_parabolic_left_relief(self) -> 'float':
        """float: 'StartOfParabolicLeftRelief' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicLeftRelief

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_left_relief.setter
    def start_of_parabolic_left_relief(self, value: 'float'):
        self.wrapped.StartOfParabolicLeftRelief = float(value) if value is not None else 0.0

    @property
    def start_of_parabolic_right_relief(self) -> 'float':
        """float: 'StartOfParabolicRightRelief' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicRightRelief

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_right_relief.setter
    def start_of_parabolic_right_relief(self, value: 'float'):
        self.wrapped.StartOfParabolicRightRelief = float(value) if value is not None else 0.0

    @property
    def start_of_parabolic_side_relief(self) -> 'Optional[float]':
        """Optional[float]: 'StartOfParabolicSideRelief' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicSideRelief

        if temp is None:
            return None

        return temp

    @start_of_parabolic_side_relief.setter
    def start_of_parabolic_side_relief(self, value: 'Optional[float]'):
        self.wrapped.StartOfParabolicSideRelief = value

    @property
    def use_measured_data(self) -> 'bool':
        """bool: 'UseMeasuredData' is the original name of this property."""

        temp = self.wrapped.UseMeasuredData

        if temp is None:
            return False

        return temp

    @use_measured_data.setter
    def use_measured_data(self, value: 'bool'):
        self.wrapped.UseMeasuredData = bool(value) if value is not None else False

    def relief_of(self, face_width: 'float') -> 'float':
        """ 'ReliefOf' is the original name of this method.

        Args:
            face_width (float)

        Returns:
            float
        """

        face_width = float(face_width)
        method_result = self.wrapped.ReliefOf(face_width if face_width else 0.0)
        return method_result
