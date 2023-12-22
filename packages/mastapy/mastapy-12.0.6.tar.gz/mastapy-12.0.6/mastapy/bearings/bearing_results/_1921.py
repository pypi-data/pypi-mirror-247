﻿"""_1921.py

LoadedNonLinearBearingResults
"""


from mastapy.materials.efficiency import (
    _296, _289, _291, _297,
    _287, _290
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results import _1913
from mastapy._internal.python_net import python_net_import

_LOADED_NON_LINEAR_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedNonLinearBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedNonLinearBearingResults',)


class LoadedNonLinearBearingResults(_1913.LoadedBearingResults):
    """LoadedNonLinearBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_NON_LINEAR_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedNonLinearBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def power_loss(self) -> '_296.PowerLoss':
        """PowerLoss: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoss

        if temp is None:
            return None

        if _296.PowerLoss.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_loss to PowerLoss. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_loss_of_type_independent_power_loss(self) -> '_289.IndependentPowerLoss':
        """IndependentPowerLoss: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoss

        if temp is None:
            return None

        if _289.IndependentPowerLoss.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_loss to IndependentPowerLoss. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_loss_of_type_load_and_speed_combined_power_loss(self) -> '_291.LoadAndSpeedCombinedPowerLoss':
        """LoadAndSpeedCombinedPowerLoss: 'PowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerLoss

        if temp is None:
            return None

        if _291.LoadAndSpeedCombinedPowerLoss.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast power_loss to LoadAndSpeedCombinedPowerLoss. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def resistive_torque(self) -> '_297.ResistiveTorque':
        """ResistiveTorque: 'ResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResistiveTorque

        if temp is None:
            return None

        if _297.ResistiveTorque.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast resistive_torque to ResistiveTorque. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def resistive_torque_of_type_combined_resistive_torque(self) -> '_287.CombinedResistiveTorque':
        """CombinedResistiveTorque: 'ResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResistiveTorque

        if temp is None:
            return None

        if _287.CombinedResistiveTorque.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast resistive_torque to CombinedResistiveTorque. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def resistive_torque_of_type_independent_resistive_torque(self) -> '_290.IndependentResistiveTorque':
        """IndependentResistiveTorque: 'ResistiveTorque' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResistiveTorque

        if temp is None:
            return None

        if _290.IndependentResistiveTorque.TYPE not in temp.__class__.__mro__:
            raise CastException('Failed to cast resistive_torque to IndependentResistiveTorque. Expected: {}.'.format(temp.__class__.__qualname__))

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
