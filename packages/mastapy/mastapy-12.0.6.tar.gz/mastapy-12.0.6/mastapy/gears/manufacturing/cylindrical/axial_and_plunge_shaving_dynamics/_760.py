﻿"""_760.py

ShavingDynamicsCalculationForDesignedGears
"""


from typing import List, Generic, TypeVar

from mastapy.utility_gui.charts import (
    _1830, _1816, _1823, _1825
)
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.gears.gear_designs.cylindrical import _1018
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _757, _743, _750, _754,
    _759, _758
)

_REPORTING_OVERRIDABLE = python_net_import('SMT.MastaAPI.Utility.Property', 'ReportingOverridable')
_SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamicsCalculationForDesignedGears')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamicsCalculationForDesignedGears',)


T = TypeVar('T', bound='_758.ShavingDynamics')


class ShavingDynamicsCalculationForDesignedGears(_759.ShavingDynamicsCalculation['T'], Generic[T]):
    """ShavingDynamicsCalculationForDesignedGears

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _SHAVING_DYNAMICS_CALCULATION_FOR_DESIGNED_GEARS

    def __init__(self, instance_to_wrap: 'ShavingDynamicsCalculationForDesignedGears.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def redressing_chart(self) -> '_1830.TwoDChartDefinition':
        """TwoDChartDefinition: 'RedressingChart' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RedressingChart

        if temp is None:
            return None

        if _1830.TwoDChartDefinition.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast redressing_chart to TwoDChartDefinition. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def selected_redressing(self) -> 'list_with_selected_item.ListWithSelectedItem_T':
        """list_with_selected_item.ListWithSelectedItem_T: 'SelectedRedressing' is the original name of this property."""

        temp = self.wrapped.SelectedRedressing

        if temp is None:
            return None

        return constructor.new_from_mastapy_type(list_with_selected_item.ListWithSelectedItem_T)(temp) if temp is not None else None

    @selected_redressing.setter
    def selected_redressing(self, value: 'list_with_selected_item.ListWithSelectedItem_T.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_T.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_T.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value is not None else None)
        self.wrapped.SelectedRedressing = value

    @property
    def end_of_shaving_profile(self) -> '_1018.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'EndOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EndOfShavingProfile.Value

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def redressing(self) -> '_757.ShaverRedressing[T]':
        """ShaverRedressing[T]: 'Redressing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Redressing

        if temp is None:
            return None

        if _757.ShaverRedressing[T].TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast redressing to ShaverRedressing[T]. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)[T](temp) if temp is not None else None

    @property
    def redressing_of_type_axial_shaver_redressing(self) -> '_743.AxialShaverRedressing':
        """AxialShaverRedressing: 'Redressing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Redressing

        if temp is None:
            return None

        if _743.AxialShaverRedressing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast redressing to AxialShaverRedressing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def redressing_of_type_plunge_shaver_redressing(self) -> '_750.PlungeShaverRedressing':
        """PlungeShaverRedressing: 'Redressing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Redressing

        if temp is None:
            return None

        if _750.PlungeShaverRedressing.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast redressing to PlungeShaverRedressing. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def start_of_shaving_profile(self) -> '_1018.CylindricalGearProfileMeasurement':
        """CylindricalGearProfileMeasurement: 'StartOfShavingProfile' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StartOfShavingProfile.Value

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def redressing_settings(self) -> 'List[_754.RedressingSettings[T]]':
        """List[RedressingSettings[T]]: 'RedressingSettings' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RedressingSettings

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
