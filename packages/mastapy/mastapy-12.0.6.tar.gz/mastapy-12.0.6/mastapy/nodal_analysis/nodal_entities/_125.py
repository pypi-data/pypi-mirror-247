﻿"""_125.py

Bar
"""


from mastapy._internal import constructor
from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy.nodal_analysis import _51
from mastapy.nodal_analysis.nodal_entities import _141
from mastapy._internal.python_net import python_net_import

_BAR = python_net_import('SMT.MastaAPI.NodalAnalysis.NodalEntities', 'Bar')


__docformat__ = 'restructuredtext en'
__all__ = ('Bar',)


class Bar(_141.NodalComponent):
    """Bar

    This is a mastapy class.
    """

    TYPE = _BAR

    def __init__(self, instance_to_wrap: 'Bar.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def oil_dip_coefficient_inner(self) -> 'float':
        """float: 'OilDipCoefficientInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilDipCoefficientInner

        if temp is None:
            return 0.0

        return temp

    @property
    def oil_dip_coefficient_outer(self) -> 'float':
        """float: 'OilDipCoefficientOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.OilDipCoefficientOuter

        if temp is None:
            return 0.0

        return temp

    @property
    def torsional_compliance(self) -> 'float':
        """float: 'TorsionalCompliance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorsionalCompliance

        if temp is None:
            return 0.0

        return temp

    @property
    def torsional_stiffness(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'TorsionalStiffness' is the original name of this property."""

        temp = self.wrapped.TorsionalStiffness

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.TorsionalStiffness = value

    @property
    def windage_loss_resistive_torque_inner(self) -> 'float':
        """float: 'WindageLossResistiveTorqueInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WindageLossResistiveTorqueInner

        if temp is None:
            return 0.0

        return temp

    @property
    def windage_loss_resistive_torque_outer(self) -> 'float':
        """float: 'WindageLossResistiveTorqueOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WindageLossResistiveTorqueOuter

        if temp is None:
            return 0.0

        return temp

    @property
    def windage_power_loss_inner(self) -> 'float':
        """float: 'WindagePowerLossInner' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WindagePowerLossInner

        if temp is None:
            return 0.0

        return temp

    @property
    def windage_power_loss_outer(self) -> 'float':
        """float: 'WindagePowerLossOuter' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WindagePowerLossOuter

        if temp is None:
            return 0.0

        return temp

    @property
    def bar_geometry(self) -> '_51.BarGeometry':
        """BarGeometry: 'BarGeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BarGeometry

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
