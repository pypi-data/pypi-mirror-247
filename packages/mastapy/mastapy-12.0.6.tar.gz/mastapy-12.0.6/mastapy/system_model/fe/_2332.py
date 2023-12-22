﻿"""_2332.py

ElectricMachineDataSet
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.fe import _2343
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.system_model.analyses_and_results.static_loads import _6908
from mastapy.electric_machines.harmonic_load_data import _1350
from mastapy.units_and_measurements import _7490
from mastapy._internal.python_net import python_net_import
from mastapy.math_utility import _1487
from mastapy import _0

_ARRAY = python_net_import('System', 'Array')
_DOUBLE = python_net_import('System', 'Double')
_STRING = python_net_import('System', 'String')
_HARMONIC_LOAD_DATA_TYPE = python_net_import('SMT.MastaAPI.ElectricMachines.HarmonicLoadData', 'HarmonicLoadDataType')
_FE_SUBSTRUCTURE_NODE = python_net_import('SMT.MastaAPI.SystemModel.FE', 'FESubstructureNode')
_ELECTRIC_MACHINE_DATA_SET = python_net_import('SMT.MastaAPI.SystemModel.FE', 'ElectricMachineDataSet')
_LIST = python_net_import('System.Collections.Generic', 'List')
_MEASUREMENT_TYPE = python_net_import('SMT.MastaAPIUtility.UnitsAndMeasurements', 'MeasurementType')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineDataSet',)


class ElectricMachineDataSet(_0.APIBase):
    """ElectricMachineDataSet

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_DATA_SET

    def __init__(self, instance_to_wrap: 'ElectricMachineDataSet.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def data_set_name(self) -> 'str':
        """str: 'DataSetName' is the original name of this property."""

        temp = self.wrapped.DataSetName

        if temp is None:
            return ''

        return temp

    @data_set_name.setter
    def data_set_name(self, value: 'str'):
        self.wrapped.DataSetName = str(value) if value is not None else ''

    @property
    def node_for_first_tooth(self) -> 'list_with_selected_item.ListWithSelectedItem_FESubstructureNode':
        """list_with_selected_item.ListWithSelectedItem_FESubstructureNode: 'NodeForFirstTooth' is the original name of this property."""

        temp = self.wrapped.NodeForFirstTooth

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_FESubstructureNode)(temp) if temp is not None else None

    @node_for_first_tooth.setter
    def node_for_first_tooth(self, value: 'list_with_selected_item.ListWithSelectedItem_FESubstructureNode.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_FESubstructureNode.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.NodeForFirstTooth = value

    @property
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(self) -> 'float':
        """float: 'RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off.setter
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def rotor_x_force_amplitude_cut_off(self) -> 'float':
        """float: 'RotorXForceAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorXForceAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @rotor_x_force_amplitude_cut_off.setter
    def rotor_x_force_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorXForceAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def rotor_y_force_amplitude_cut_off(self) -> 'float':
        """float: 'RotorYForceAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorYForceAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @rotor_y_force_amplitude_cut_off.setter
    def rotor_y_force_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorYForceAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def rotor_z_force_amplitude_cut_off(self) -> 'float':
        """float: 'RotorZForceAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.RotorZForceAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @rotor_z_force_amplitude_cut_off.setter
    def rotor_z_force_amplitude_cut_off(self, value: 'float'):
        self.wrapped.RotorZForceAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def stator_axial_loads_amplitude_cut_off(self) -> 'float':
        """float: 'StatorAxialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.StatorAxialLoadsAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @stator_axial_loads_amplitude_cut_off.setter
    def stator_axial_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.StatorAxialLoadsAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def stator_radial_loads_amplitude_cut_off(self) -> 'float':
        """float: 'StatorRadialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.StatorRadialLoadsAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @stator_radial_loads_amplitude_cut_off.setter
    def stator_radial_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.StatorRadialLoadsAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def stator_tangential_loads_amplitude_cut_off(self) -> 'float':
        """float: 'StatorTangentialLoadsAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.StatorTangentialLoadsAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @stator_tangential_loads_amplitude_cut_off.setter
    def stator_tangential_loads_amplitude_cut_off(self, value: 'float'):
        self.wrapped.StatorTangentialLoadsAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def torque_ripple_amplitude_cut_off(self) -> 'float':
        """float: 'TorqueRippleAmplitudeCutOff' is the original name of this property."""

        temp = self.wrapped.TorqueRippleAmplitudeCutOff

        if temp is None:
            return 0.0

        return temp

    @torque_ripple_amplitude_cut_off.setter
    def torque_ripple_amplitude_cut_off(self, value: 'float'):
        self.wrapped.TorqueRippleAmplitudeCutOff = float(value) if value is not None else 0.0

    @property
    def torque_ripple_input_type(self) -> '_6908.TorqueRippleInputType':
        """TorqueRippleInputType: 'TorqueRippleInputType' is the original name of this property."""

        temp = self.wrapped.TorqueRippleInputType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_6908.TorqueRippleInputType)(value) if value is not None else None

    @torque_ripple_input_type.setter
    def torque_ripple_input_type(self, value: '_6908.TorqueRippleInputType'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.TorqueRippleInputType = value

    @property
    def report_names(self) -> 'List[str]':
        """List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def delete_data_set(self):
        """ 'DeleteDataSet' is the original name of this method."""

        self.wrapped.DeleteDataSet()

    def add_or_replace_excitation_data_with_amplitudes_phases_and_fe_node(self, harmonic_load_data_type: '_1350.HarmonicLoadDataType', node: '_2343.FESubstructureNode', speed: 'float', fourier_series_amplitudes: 'List[float]', fourier_series_phases: 'List[float]', fourier_series_mean_value: 'float', fourier_series_name: 'str', fourier_series_measurement_type: '_7490.MeasurementType'):
        """ 'AddOrReplaceExcitationData' is the original name of this method.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            node (mastapy.system_model.fe.FESubstructureNode)
            speed (float)
            fourier_series_amplitudes (List[float])
            fourier_series_phases (List[float])
            fourier_series_mean_value (float)
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """

        harmonic_load_data_type = conversion.mp_to_pn_enum(harmonic_load_data_type)
        speed = float(speed)
        fourier_series_amplitudes = conversion.mp_to_pn_list_float(fourier_series_amplitudes)
        fourier_series_phases = conversion.mp_to_pn_list_float(fourier_series_phases)
        fourier_series_mean_value = float(fourier_series_mean_value)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.AddOrReplaceExcitationData.Overloads[_HARMONIC_LOAD_DATA_TYPE, _FE_SUBSTRUCTURE_NODE, _DOUBLE, _LIST[_DOUBLE], _LIST[_DOUBLE], _DOUBLE, _STRING, _MEASUREMENT_TYPE](harmonic_load_data_type, node.wrapped if node else None, speed if speed else 0.0, fourier_series_amplitudes, fourier_series_phases, fourier_series_mean_value if fourier_series_mean_value else 0.0, fourier_series_name if fourier_series_name else '', fourier_series_measurement_type)

    def add_or_replace_excitation_data_with_fe_node(self, harmonic_load_data_type: '_1350.HarmonicLoadDataType', node: '_2343.FESubstructureNode', speed: 'float', fourier_series_values: 'List[float]', fourier_series_name: 'str', fourier_series_measurement_type: '_7490.MeasurementType'):
        """ 'AddOrReplaceExcitationData' is the original name of this method.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            node (mastapy.system_model.fe.FESubstructureNode)
            speed (float)
            fourier_series_values (List[float])
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """

        harmonic_load_data_type = conversion.mp_to_pn_enum(harmonic_load_data_type)
        speed = float(speed)
        fourier_series_values = conversion.mp_to_pn_array_float(fourier_series_values)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.AddOrReplaceExcitationData.Overloads[_HARMONIC_LOAD_DATA_TYPE, _FE_SUBSTRUCTURE_NODE, _DOUBLE, _ARRAY[_DOUBLE], _STRING, _MEASUREMENT_TYPE](harmonic_load_data_type, node.wrapped if node else None, speed if speed else 0.0, fourier_series_values, fourier_series_name if fourier_series_name else '', fourier_series_measurement_type)

    def add_or_replace_excitation_data_with_amplitudes_and_phases(self, harmonic_load_data_type: '_1350.HarmonicLoadDataType', speed: 'float', fourier_series_amplitudes: 'List[float]', fourier_series_phases: 'List[float]', fourier_series_mean_value: 'float', fourier_series_name: 'str', fourier_series_measurement_type: '_7490.MeasurementType'):
        """ 'AddOrReplaceExcitationData' is the original name of this method.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            speed (float)
            fourier_series_amplitudes (List[float])
            fourier_series_phases (List[float])
            fourier_series_mean_value (float)
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """

        harmonic_load_data_type = conversion.mp_to_pn_enum(harmonic_load_data_type)
        speed = float(speed)
        fourier_series_amplitudes = conversion.mp_to_pn_list_float(fourier_series_amplitudes)
        fourier_series_phases = conversion.mp_to_pn_list_float(fourier_series_phases)
        fourier_series_mean_value = float(fourier_series_mean_value)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.AddOrReplaceExcitationData.Overloads[_HARMONIC_LOAD_DATA_TYPE, _DOUBLE, _LIST[_DOUBLE], _LIST[_DOUBLE], _DOUBLE, _STRING, _MEASUREMENT_TYPE](harmonic_load_data_type, speed if speed else 0.0, fourier_series_amplitudes, fourier_series_phases, fourier_series_mean_value if fourier_series_mean_value else 0.0, fourier_series_name if fourier_series_name else '', fourier_series_measurement_type)

    def add_or_replace_excitation_data(self, harmonic_load_data_type: '_1350.HarmonicLoadDataType', speed: 'float', fourier_series_values: 'List[float]', fourier_series_name: 'str', fourier_series_measurement_type: '_7490.MeasurementType'):
        """ 'AddOrReplaceExcitationData' is the original name of this method.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            speed (float)
            fourier_series_values (List[float])
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """

        harmonic_load_data_type = conversion.mp_to_pn_enum(harmonic_load_data_type)
        speed = float(speed)
        fourier_series_values = conversion.mp_to_pn_array_float(fourier_series_values)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(fourier_series_measurement_type)
        self.wrapped.AddOrReplaceExcitationData.Overloads[_HARMONIC_LOAD_DATA_TYPE, _DOUBLE, _ARRAY[_DOUBLE], _STRING, _MEASUREMENT_TYPE](harmonic_load_data_type, speed if speed else 0.0, fourier_series_values, fourier_series_name if fourier_series_name else '', fourier_series_measurement_type)

    def clear_all_data(self):
        """ 'ClearAllData' is the original name of this method."""

        self.wrapped.ClearAllData()

    def delete(self):
        """ 'Delete' is the original name of this method."""

        self.wrapped.Delete()

    def derive_rotor_forces_from_stator_loads(self):
        """ 'DeriveRotorForcesFromStatorLoads' is the original name of this method."""

        self.wrapped.DeriveRotorForcesFromStatorLoads()

    def derive_rotor_moments_interpolators_from_stator_axial_loads_interpolators(self):
        """ 'DeriveRotorMomentsInterpolatorsFromStatorAxialLoadsInterpolators' is the original name of this method."""

        self.wrapped.DeriveRotorMomentsInterpolatorsFromStatorAxialLoadsInterpolators()

    def derive_rotor_z_force_interpolator_from_stator_axial_load_interpolators(self):
        """ 'DeriveRotorZForceInterpolatorFromStatorAxialLoadInterpolators' is the original name of this method."""

        self.wrapped.DeriveRotorZForceInterpolatorFromStatorAxialLoadInterpolators()

    def derive_stator_tangential_load_interpolators_from_torque_ripple_interpolators(self):
        """ 'DeriveStatorTangentialLoadInterpolatorsFromTorqueRippleInterpolators' is the original name of this method."""

        self.wrapped.DeriveStatorTangentialLoadInterpolatorsFromTorqueRippleInterpolators()

    def derive_torque_ripple_interpolator_from_stator_tangential_load_interpolators(self):
        """ 'DeriveTorqueRippleInterpolatorFromStatorTangentialLoadInterpolators' is the original name of this method."""

        self.wrapped.DeriveTorqueRippleInterpolatorFromStatorTangentialLoadInterpolators()

    def multiple_fourier_series_interpolator_for(self, harmonic_load_data_type: '_1350.HarmonicLoadDataType') -> '_1487.MultipleFourierSeriesInterpolator':
        """ 'MultipleFourierSeriesInterpolatorFor' is the original name of this method.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)

        Returns:
            mastapy.math_utility.MultipleFourierSeriesInterpolator
        """

        harmonic_load_data_type = conversion.mp_to_pn_enum(harmonic_load_data_type)
        method_result = self.wrapped.MultipleFourierSeriesInterpolatorFor.Overloads[_HARMONIC_LOAD_DATA_TYPE](harmonic_load_data_type)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def multiple_fourier_series_interpolator_for_with_fe_node(self, harmonic_load_data_type: '_1350.HarmonicLoadDataType', node: '_2343.FESubstructureNode') -> '_1487.MultipleFourierSeriesInterpolator':
        """ 'MultipleFourierSeriesInterpolatorFor' is the original name of this method.

        Args:
            harmonic_load_data_type (mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType)
            node (mastapy.system_model.fe.FESubstructureNode)

        Returns:
            mastapy.math_utility.MultipleFourierSeriesInterpolator
        """

        harmonic_load_data_type = conversion.mp_to_pn_enum(harmonic_load_data_type)
        method_result = self.wrapped.MultipleFourierSeriesInterpolatorFor.Overloads[_HARMONIC_LOAD_DATA_TYPE, _FE_SUBSTRUCTURE_NODE](harmonic_load_data_type, node.wrapped if node else None)
        type_ = method_result.GetType()
        return constructor.new(type_.Namespace, type_.Name)(method_result) if method_result is not None else None

    def output_default_report_to(self, file_path: 'str'):
        """ 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else '')

    def get_default_report_with_encoded_images(self) -> 'str':
        """ 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        """ 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else '')

    def output_active_report_as_text_to(self, file_path: 'str'):
        """ 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        """

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else '')

    def get_active_report_with_encoded_images(self) -> 'str':
        """ 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        """

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else '', file_path if file_path else '')

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        """ 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        """

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else '', file_path if file_path else '')

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        """ 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        """

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else '')
        return method_result
