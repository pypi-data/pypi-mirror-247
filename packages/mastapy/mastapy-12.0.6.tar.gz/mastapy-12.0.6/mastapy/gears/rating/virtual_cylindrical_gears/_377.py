﻿"""_377.py

HypoidVirtualCylindricalGearSetISO10300MethodB2
"""


from mastapy._internal import constructor
from mastapy.gears.rating.virtual_cylindrical_gears import _388
from mastapy._internal.python_net import python_net_import

_HYPOID_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2 = python_net_import('SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears', 'HypoidVirtualCylindricalGearSetISO10300MethodB2')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidVirtualCylindricalGearSetISO10300MethodB2',)


class HypoidVirtualCylindricalGearSetISO10300MethodB2(_388.VirtualCylindricalGearSetISO10300MethodB2):
    """HypoidVirtualCylindricalGearSetISO10300MethodB2

    This is a mastapy class.
    """

    TYPE = _HYPOID_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2

    def __init__(self, instance_to_wrap: 'HypoidVirtualCylindricalGearSetISO10300MethodB2.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angle_between_direction_of_contact_and_the_pitch_tangent(self) -> 'float':
        """float: 'AngleBetweenDirectionOfContactAndThePitchTangent' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngleBetweenDirectionOfContactAndThePitchTangent

        if temp is None:
            return 0.0

        return temp

    @property
    def average_pressure_angle_unbalance(self) -> 'float':
        """float: 'AveragePressureAngleUnbalance' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AveragePressureAngleUnbalance

        if temp is None:
            return 0.0

        return temp

    @property
    def coast_flank_pressure_angel_in_wheel_root_coordinates(self) -> 'float':
        """float: 'CoastFlankPressureAngelInWheelRootCoordinates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CoastFlankPressureAngelInWheelRootCoordinates

        if temp is None:
            return 0.0

        return temp

    @property
    def drive_flank_pressure_angel_in_wheel_root_coordinates(self) -> 'float':
        """float: 'DriveFlankPressureAngelInWheelRootCoordinates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DriveFlankPressureAngelInWheelRootCoordinates

        if temp is None:
            return 0.0

        return temp

    @property
    def initial_value_for_the_wheel_angle_from_centreline_to_fillet_point_on_drive_flank(self) -> 'float':
        """float: 'InitialValueForTheWheelAngleFromCentrelineToFilletPointOnDriveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InitialValueForTheWheelAngleFromCentrelineToFilletPointOnDriveFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def length_of_action_from_pinion_tip_to_pitch_circle_in_normal_section(self) -> 'float':
        """float: 'LengthOfActionFromPinionTipToPitchCircleInNormalSection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfActionFromPinionTipToPitchCircleInNormalSection

        if temp is None:
            return 0.0

        return temp

    @property
    def length_of_action_from_wheel_tip_to_pitch_circle_in_normal_section(self) -> 'float':
        """float: 'LengthOfActionFromWheelTipToPitchCircleInNormalSection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LengthOfActionFromWheelTipToPitchCircleInNormalSection

        if temp is None:
            return 0.0

        return temp

    @property
    def limit_pressure_angle_in_wheel_root_coordinates(self) -> 'float':
        """float: 'LimitPressureAngleInWheelRootCoordinates' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LimitPressureAngleInWheelRootCoordinates

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_contact_ratio_for_hypoid_gears(self) -> 'float':
        """float: 'ModifiedContactRatioForHypoidGears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedContactRatioForHypoidGears

        if temp is None:
            return 0.0

        return temp

    @property
    def relative_distance_from_blade_edge_to_centreline(self) -> 'float':
        """float: 'RelativeDistanceFromBladeEdgeToCentreline' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeDistanceFromBladeEdgeToCentreline

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_angle_from_centreline_to_fillet_point_on_drive_flank(self) -> 'float':
        """float: 'WheelAngleFromCentrelineToFilletPointOnDriveFlank' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelAngleFromCentrelineToFilletPointOnDriveFlank

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_angle_from_centreline_to_pinion_tip_on_drive_side(self) -> 'float':
        """float: 'WheelAngleFromCentrelineToPinionTipOnDriveSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelAngleFromCentrelineToPinionTipOnDriveSide

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_angle_from_centreline_to_tooth_surface_at_pitch_point_on_drive_side(self) -> 'float':
        """float: 'WheelAngleFromCentrelineToToothSurfaceAtPitchPointOnDriveSide' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelAngleFromCentrelineToToothSurfaceAtPitchPointOnDriveSide

        if temp is None:
            return 0.0

        return temp

    @property
    def wheel_mean_slot_width(self) -> 'float':
        """float: 'WheelMeanSlotWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WheelMeanSlotWidth

        if temp is None:
            return 0.0

        return temp

    @property
    def h(self) -> 'float':
        """float: 'H' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.H

        if temp is None:
            return 0.0

        return temp

    @property
    def h1(self) -> 'float':
        """float: 'H1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.H1

        if temp is None:
            return 0.0

        return temp

    @property
    def h1o(self) -> 'float':
        """float: 'H1o' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.H1o

        if temp is None:
            return 0.0

        return temp

    @property
    def h2(self) -> 'float':
        """float: 'H2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.H2

        if temp is None:
            return 0.0

        return temp

    @property
    def h2o(self) -> 'float':
        """float: 'H2o' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.H2o

        if temp is None:
            return 0.0

        return temp

    @property
    def deltar(self) -> 'float':
        """float: 'Deltar' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Deltar

        if temp is None:
            return 0.0

        return temp

    @property
    def deltar_1(self) -> 'float':
        """float: 'Deltar1' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Deltar1

        if temp is None:
            return 0.0

        return temp

    @property
    def deltar_2(self) -> 'float':
        """float: 'Deltar2' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Deltar2

        if temp is None:
            return 0.0

        return temp
