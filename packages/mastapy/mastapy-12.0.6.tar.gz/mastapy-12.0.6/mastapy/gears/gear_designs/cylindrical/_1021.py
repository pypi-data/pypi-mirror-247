﻿"""_1021.py

CylindricalGearSetDesign
"""


from typing import List, Optional

from mastapy._internal import constructor, conversion, enum_with_selected_value_runtime
from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy.gears import _313
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.materials.efficiency import _288
from mastapy._internal.python_net import python_net_import
from mastapy.gears.gear_designs.cylindrical import (
    _1039, _991, _1015, _1052,
    _1022, _1055, _1062, _1080,
    _1005, _1011, _1023
)
from mastapy.gears.rating.cylindrical.iso6336 import _503
from mastapy.gears.manufacturing.cylindrical import _618
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1099
from mastapy.gears.rating.cylindrical import _448, _457
from mastapy.gears.gear_designs import _943

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetDesign',)


class CylindricalGearSetDesign(_943.GearSetDesign):
    """CylindricalGearSetDesign

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_SET_DESIGN

    def __init__(self, instance_to_wrap: 'CylindricalGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def all_gears_number_of_teeth(self) -> 'List[int]':
        """List[int]: 'AllGearsNumberOfTeeth' is the original name of this property."""

        temp = self.wrapped.AllGearsNumberOfTeeth

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)
        return value

    @all_gears_number_of_teeth.setter
    def all_gears_number_of_teeth(self, value: 'List[int]'):
        value = conversion.mp_to_pn_objects_in_list(value)
        self.wrapped.AllGearsNumberOfTeeth = value

    @property
    def axial_pitch(self) -> 'float':
        """float: 'AxialPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AxialPitch

        if temp is None:
            return 0.0

        return temp

    @property
    def coefficient_of_friction_calculation_method(self) -> 'overridable.Overridable_CoefficientOfFrictionCalculationMethod':
        """overridable.Overridable_CoefficientOfFrictionCalculationMethod: 'CoefficientOfFrictionCalculationMethod' is the original name of this property."""

        temp = self.wrapped.CoefficientOfFrictionCalculationMethod

        if temp is None:
            return None

        value = overridable.Overridable_CoefficientOfFrictionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value) if temp is not None else None

    @coefficient_of_friction_calculation_method.setter
    def coefficient_of_friction_calculation_method(self, value: 'overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()'):
        wrapper_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.wrapper_type()
        enclosed_type = overridable.Overridable_CoefficientOfFrictionCalculationMethod.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value is not None else None, is_overridden)
        self.wrapped.CoefficientOfFrictionCalculationMethod = value

    @property
    def diametral_pitch_per_inch(self) -> 'float':
        """float: 'DiametralPitchPerInch' is the original name of this property."""

        temp = self.wrapped.DiametralPitchPerInch

        if temp is None:
            return 0.0

        return temp

    @diametral_pitch_per_inch.setter
    def diametral_pitch_per_inch(self, value: 'float'):
        self.wrapped.DiametralPitchPerInch = float(value) if value is not None else 0.0

    @property
    def diametral_pitch_per_inch_with_centre_distance_adjustment(self) -> 'float':
        """float: 'DiametralPitchPerInchWithCentreDistanceAdjustment' is the original name of this property."""

        temp = self.wrapped.DiametralPitchPerInchWithCentreDistanceAdjustment

        if temp is None:
            return 0.0

        return temp

    @diametral_pitch_per_inch_with_centre_distance_adjustment.setter
    def diametral_pitch_per_inch_with_centre_distance_adjustment(self, value: 'float'):
        self.wrapped.DiametralPitchPerInchWithCentreDistanceAdjustment = float(value) if value is not None else 0.0

    @property
    def efficiency_rating_method(self) -> '_288.EfficiencyRatingMethod':
        """EfficiencyRatingMethod: 'EfficiencyRatingMethod' is the original name of this property."""

        temp = self.wrapped.EfficiencyRatingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_288.EfficiencyRatingMethod)(value) if value is not None else None

    @efficiency_rating_method.setter
    def efficiency_rating_method(self, value: '_288.EfficiencyRatingMethod'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.EfficiencyRatingMethod = value

    @property
    def fe_model_for_tiff(self) -> 'str':
        """str: 'FEModelForTIFF' is the original name of this property."""

        temp = self.wrapped.FEModelForTIFF.SelectedItemName

        if temp is None:
            return ''

        return temp

    @fe_model_for_tiff.setter
    def fe_model_for_tiff(self, value: 'str'):
        self.wrapped.FEModelForTIFF.SetSelectedItem(str(value) if value is not None else '')

    @property
    def face_width(self) -> 'Optional[float]':
        """Optional[float]: 'FaceWidth' is the original name of this property."""

        temp = self.wrapped.FaceWidth

        if temp is None:
            return None

        return temp

    @face_width.setter
    def face_width(self, value: 'Optional[float]'):
        self.wrapped.FaceWidth = value

    @property
    def gear_fit_system(self) -> '_1039.GearFitSystems':
        """GearFitSystems: 'GearFitSystem' is the original name of this property."""

        temp = self.wrapped.GearFitSystem

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1039.GearFitSystems)(value) if value is not None else None

    @gear_fit_system.setter
    def gear_fit_system(self, value: '_1039.GearFitSystems'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.GearFitSystem = value

    @property
    def gear_tooth_thickness_reduction_allowance(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'GearToothThicknessReductionAllowance' is the original name of this property."""

        temp = self.wrapped.GearToothThicknessReductionAllowance

        if temp is None:
            return ''

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else ''

    @gear_tooth_thickness_reduction_allowance.setter
    def gear_tooth_thickness_reduction_allowance(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.GearToothThicknessReductionAllowance = value

    @property
    def gear_tooth_thickness_tolerance(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        """list_with_selected_item.ListWithSelectedItem_str: 'GearToothThicknessTolerance' is the original name of this property."""

        temp = self.wrapped.GearToothThicknessTolerance

        if temp is None:
            return ''

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_str)(temp) if temp is not None else ''

    @gear_tooth_thickness_tolerance.setter
    def gear_tooth_thickness_tolerance(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else '')
        self.wrapped.GearToothThicknessTolerance = value

    @property
    def helical_gear_micro_geometry_option(self) -> '_503.HelicalGearMicroGeometryOption':
        """HelicalGearMicroGeometryOption: 'HelicalGearMicroGeometryOption' is the original name of this property."""

        temp = self.wrapped.HelicalGearMicroGeometryOption

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_503.HelicalGearMicroGeometryOption)(value) if value is not None else None

    @helical_gear_micro_geometry_option.setter
    def helical_gear_micro_geometry_option(self, value: '_503.HelicalGearMicroGeometryOption'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HelicalGearMicroGeometryOption = value

    @property
    def helix_angle(self) -> 'float':
        """float: 'HelixAngle' is the original name of this property."""

        temp = self.wrapped.HelixAngle

        if temp is None:
            return 0.0

        return temp

    @helix_angle.setter
    def helix_angle(self, value: 'float'):
        self.wrapped.HelixAngle = float(value) if value is not None else 0.0

    @property
    def helix_angle_maintain_transverse_profile(self) -> 'float':
        """float: 'HelixAngleMaintainTransverseProfile' is the original name of this property."""

        temp = self.wrapped.HelixAngleMaintainTransverseProfile

        if temp is None:
            return 0.0

        return temp

    @helix_angle_maintain_transverse_profile.setter
    def helix_angle_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.HelixAngleMaintainTransverseProfile = float(value) if value is not None else 0.0

    @property
    def helix_angle_calculating_gear_teeth_numbers(self) -> 'float':
        """float: 'HelixAngleCalculatingGearTeethNumbers' is the original name of this property."""

        temp = self.wrapped.HelixAngleCalculatingGearTeethNumbers

        if temp is None:
            return 0.0

        return temp

    @helix_angle_calculating_gear_teeth_numbers.setter
    def helix_angle_calculating_gear_teeth_numbers(self, value: 'float'):
        self.wrapped.HelixAngleCalculatingGearTeethNumbers = float(value) if value is not None else 0.0

    @property
    def helix_angle_with_centre_distance_adjustment(self) -> 'float':
        """float: 'HelixAngleWithCentreDistanceAdjustment' is the original name of this property."""

        temp = self.wrapped.HelixAngleWithCentreDistanceAdjustment

        if temp is None:
            return 0.0

        return temp

    @helix_angle_with_centre_distance_adjustment.setter
    def helix_angle_with_centre_distance_adjustment(self, value: 'float'):
        self.wrapped.HelixAngleWithCentreDistanceAdjustment = float(value) if value is not None else 0.0

    @property
    def is_asymmetric(self) -> 'bool':
        """bool: 'IsAsymmetric' is the original name of this property."""

        temp = self.wrapped.IsAsymmetric

        if temp is None:
            return False

        return temp

    @is_asymmetric.setter
    def is_asymmetric(self, value: 'bool'):
        self.wrapped.IsAsymmetric = bool(value) if value is not None else False

    @property
    def minimum_axial_contact_ratio(self) -> 'float':
        """float: 'MinimumAxialContactRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumAxialContactRatio

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_tip_thickness(self) -> 'float':
        """float: 'MinimumTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MinimumTipThickness

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_module(self) -> 'float':
        """float: 'NormalModule' is the original name of this property."""

        temp = self.wrapped.NormalModule

        if temp is None:
            return 0.0

        return temp

    @normal_module.setter
    def normal_module(self, value: 'float'):
        self.wrapped.NormalModule = float(value) if value is not None else 0.0

    @property
    def normal_module_maintain_transverse_profile(self) -> 'float':
        """float: 'NormalModuleMaintainTransverseProfile' is the original name of this property."""

        temp = self.wrapped.NormalModuleMaintainTransverseProfile

        if temp is None:
            return 0.0

        return temp

    @normal_module_maintain_transverse_profile.setter
    def normal_module_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.NormalModuleMaintainTransverseProfile = float(value) if value is not None else 0.0

    @property
    def normal_module_calculating_gear_teeth_numbers(self) -> 'float':
        """float: 'NormalModuleCalculatingGearTeethNumbers' is the original name of this property."""

        temp = self.wrapped.NormalModuleCalculatingGearTeethNumbers

        if temp is None:
            return 0.0

        return temp

    @normal_module_calculating_gear_teeth_numbers.setter
    def normal_module_calculating_gear_teeth_numbers(self, value: 'float'):
        self.wrapped.NormalModuleCalculatingGearTeethNumbers = float(value) if value is not None else 0.0

    @property
    def normal_module_with_centre_distance_adjustment(self) -> 'float':
        """float: 'NormalModuleWithCentreDistanceAdjustment' is the original name of this property."""

        temp = self.wrapped.NormalModuleWithCentreDistanceAdjustment

        if temp is None:
            return 0.0

        return temp

    @normal_module_with_centre_distance_adjustment.setter
    def normal_module_with_centre_distance_adjustment(self, value: 'float'):
        self.wrapped.NormalModuleWithCentreDistanceAdjustment = float(value) if value is not None else 0.0

    @property
    def normal_pitch(self) -> 'float':
        """float: 'NormalPitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalPitch

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_pressure_angle_maintain_transverse_profile(self) -> 'float':
        """float: 'NormalPressureAngleMaintainTransverseProfile' is the original name of this property."""

        temp = self.wrapped.NormalPressureAngleMaintainTransverseProfile

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle_maintain_transverse_profile.setter
    def normal_pressure_angle_maintain_transverse_profile(self, value: 'float'):
        self.wrapped.NormalPressureAngleMaintainTransverseProfile = float(value) if value is not None else 0.0

    @property
    def profile_shift_distribution_rule(self) -> '_991.AddendumModificationDistributionRule':
        """AddendumModificationDistributionRule: 'ProfileShiftDistributionRule' is the original name of this property."""

        temp = self.wrapped.ProfileShiftDistributionRule

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_991.AddendumModificationDistributionRule)(value) if value is not None else None

    @profile_shift_distribution_rule.setter
    def profile_shift_distribution_rule(self, value: '_991.AddendumModificationDistributionRule'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ProfileShiftDistributionRule = value

    @property
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(self) -> 'float':
        """float: 'RootGearProfileShiftCoefficientMaintainTipAndRootDiameters' is the original name of this property."""

        temp = self.wrapped.RootGearProfileShiftCoefficientMaintainTipAndRootDiameters

        if temp is None:
            return 0.0

        return temp

    @root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters.setter
    def root_gear_profile_shift_coefficient_maintain_tip_and_root_diameters(self, value: 'float'):
        self.wrapped.RootGearProfileShiftCoefficientMaintainTipAndRootDiameters = float(value) if value is not None else 0.0

    @property
    def transverse_module(self) -> 'float':
        """float: 'TransverseModule' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseModule

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_pitch(self) -> 'float':
        """float: 'TransversePitch' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransversePitch

        if temp is None:
            return 0.0

        return temp

    @property
    def cylindrical_gear_micro_geometry_settings(self) -> '_1015.CylindricalGearMicroGeometrySettingsItem':
        """CylindricalGearMicroGeometrySettingsItem: 'CylindricalGearMicroGeometrySettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearMicroGeometrySettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_set_manufacturing_configuration(self) -> '_618.CylindricalSetManufacturingConfig':
        """CylindricalSetManufacturingConfig: 'CylindricalGearSetManufacturingConfiguration' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSetManufacturingConfiguration

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_1099.CylindricalGearSetMicroGeometry':
        """CylindricalGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGearSetMicroGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def ltca_settings(self) -> '_1052.LtcaSettings':
        """LtcaSettings: 'LTCASettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LTCASettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def left_flank(self) -> '_1022.CylindricalGearSetFlankDesign':
        """CylindricalGearSetFlankDesign: 'LeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LeftFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micropitting(self) -> '_1055.Micropitting':
        """Micropitting: 'Micropitting' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Micropitting

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def rating_settings(self) -> '_448.CylindricalGearDesignAndRatingSettingsItem':
        """CylindricalGearDesignAndRatingSettingsItem: 'RatingSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RatingSettings

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def right_flank(self) -> '_1022.CylindricalGearSetFlankDesign':
        """CylindricalGearSetFlankDesign: 'RightFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RightFlank

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def scuffing(self) -> '_1062.Scuffing':
        """Scuffing: 'Scuffing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Scuffing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def usage(self) -> '_1080.Usage':
        """Usage: 'Usage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Usage

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def gears(self) -> 'List[_1005.CylindricalGearDesign]':
        """List[CylindricalGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_gears(self) -> 'List[_1005.CylindricalGearDesign]':
        """List[CylindricalGearDesign]: 'CylindricalGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def cylindrical_meshes(self) -> 'List[_1011.CylindricalGearMeshDesign]':
        """List[CylindricalGearMeshDesign]: 'CylindricalMeshes' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CylindricalMeshes

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def flanks(self) -> 'List[_1022.CylindricalGearSetFlankDesign]':
        """List[CylindricalGearSetFlankDesign]: 'Flanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Flanks

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def both_flanks(self) -> '_1022.CylindricalGearSetFlankDesign':
        """CylindricalGearSetFlankDesign: 'BothFlanks' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BothFlanks

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def micro_geometries(self) -> 'List[_1099.CylindricalGearSetMicroGeometry]':
        """List[CylindricalGearSetMicroGeometry]: 'MicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MicroGeometries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def manufacturing_configurations(self) -> 'List[_618.CylindricalSetManufacturingConfig]':
        """List[CylindricalSetManufacturingConfig]: 'ManufacturingConfigurations' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ManufacturingConfigurations

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    def centre_distance_editor(self):
        """ 'CentreDistanceEditor' is the original name of this method."""

        self.wrapped.CentreDistanceEditor()

    def set_helix_angle_for_axial_contact_ratio(self):
        """ 'SetHelixAngleForAxialContactRatio' is the original name of this method."""

        self.wrapped.SetHelixAngleForAxialContactRatio()

    def add_new_manufacturing_configuration(self, new_config_name: Optional['str'] = 'None') -> '_618.CylindricalSetManufacturingConfig':
        """ 'AddNewManufacturingConfiguration' is the original name of this method.

        Args:
            new_config_name (str, optional)

        Returns:
            mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig
        """

        new_config_name = str(new_config_name)
        method_result = self.wrapped.AddNewManufacturingConfiguration(new_config_name if new_config_name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def add_new_micro_geometry(self) -> '_1099.CylindricalGearSetMicroGeometry':
        """ 'AddNewMicroGeometry' is the original name of this method.

        Returns:
            mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry
        """

        method_result = self.wrapped.AddNewMicroGeometry()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def add_new_micro_geometry_specifying_separate_micro_geometry_per_tooth(self) -> '_1099.CylindricalGearSetMicroGeometry':
        """ 'AddNewMicroGeometrySpecifyingSeparateMicroGeometryPerTooth' is the original name of this method.

        Returns:
            mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry
        """

        method_result = self.wrapped.AddNewMicroGeometrySpecifyingSeparateMicroGeometryPerTooth()
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def add_new_micro_geometry_specifying_separate_micro_geometry_per_tooth_for(self, gears: 'List[_1005.CylindricalGearDesign]') -> '_1099.CylindricalGearSetMicroGeometry':
        """ 'AddNewMicroGeometrySpecifyingSeparateMicroGeometryPerToothFor' is the original name of this method.

        Args:
            gears (List[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign])

        Returns:
            mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry
        """

        gears = conversion.mp_to_pn_objects_in_dotnet_list(gears)
        method_result = self.wrapped.AddNewMicroGeometrySpecifyingSeparateMicroGeometryPerToothFor(gears)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def create_optimiser(self, duty_cycle: '_457.CylindricalGearSetDutyCycleRating') -> '_1023.CylindricalGearSetMacroGeometryOptimiser':
        """ 'CreateOptimiser' is the original name of this method.

        Args:
            duty_cycle (mastapy.gears.rating.cylindrical.CylindricalGearSetDutyCycleRating)

        Returns:
            mastapy.gears.gear_designs.cylindrical.CylindricalGearSetMacroGeometryOptimiser
        """

        method_result = self.wrapped.CreateOptimiser(duty_cycle.wrapped if duty_cycle else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def delete_manufacturing_configuration(self, config: '_618.CylindricalSetManufacturingConfig'):
        """ 'DeleteManufacturingConfiguration' is the original name of this method.

        Args:
            config (mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig)
        """

        self.wrapped.DeleteManufacturingConfiguration(config.wrapped if config else None)

    def delete_micro_geometry(self, micro_geometry: '_1099.CylindricalGearSetMicroGeometry'):
        """ 'DeleteMicroGeometry' is the original name of this method.

        Args:
            micro_geometry (mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry)
        """

        self.wrapped.DeleteMicroGeometry(micro_geometry.wrapped if micro_geometry else None)

    def delete_unused_manufacturing_configurations(self):
        """ 'DeleteUnusedManufacturingConfigurations' is the original name of this method."""

        self.wrapped.DeleteUnusedManufacturingConfigurations()

    def try_make_valid(self):
        """ 'TryMakeValid' is the original name of this method."""

        self.wrapped.TryMakeValid()

    def micro_geometry_named(self, micro_geometry_name: 'str') -> '_1099.CylindricalGearSetMicroGeometry':
        """ 'MicroGeometryNamed' is the original name of this method.

        Args:
            micro_geometry_name (str)

        Returns:
            mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry
        """

        micro_geometry_name = str(micro_geometry_name)
        method_result = self.wrapped.MicroGeometryNamed(micro_geometry_name if micro_geometry_name else '')
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def set_active_manufacturing_configuration(self, value: '_618.CylindricalSetManufacturingConfig'):
        """ 'SetActiveManufacturingConfiguration' is the original name of this method.

        Args:
            value (mastapy.gears.manufacturing.cylindrical.CylindricalSetManufacturingConfig)
        """

        self.wrapped.SetActiveManufacturingConfiguration(value.wrapped if value else None)

    def set_active_micro_geometry(self, value: '_1099.CylindricalGearSetMicroGeometry'):
        """ 'SetActiveMicroGeometry' is the original name of this method.

        Args:
            value (mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometry)
        """

        self.wrapped.SetActiveMicroGeometry(value.wrapped if value else None)

    def clear_all_tooth_thickness_specifications(self):
        """ 'ClearAllToothThicknessSpecifications' is the original name of this method."""

        self.wrapped.ClearAllToothThicknessSpecifications()
