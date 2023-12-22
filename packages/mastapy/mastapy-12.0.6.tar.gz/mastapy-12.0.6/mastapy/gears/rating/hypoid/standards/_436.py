﻿"""_436.py

GleasonHypoidGearSingleFlankRating
"""


from mastapy._internal import constructor
from mastapy.gears.rating.conical import _536
from mastapy._internal.python_net import python_net_import

_GLEASON_HYPOID_GEAR_SINGLE_FLANK_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Hypoid.Standards', 'GleasonHypoidGearSingleFlankRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GleasonHypoidGearSingleFlankRating',)


class GleasonHypoidGearSingleFlankRating(_536.ConicalGearSingleFlankRating):
    """GleasonHypoidGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE = _GLEASON_HYPOID_GEAR_SINGLE_FLANK_RATING

    def __init__(self, instance_to_wrap: 'GleasonHypoidGearSingleFlankRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_safety_factor_for_fatigue(self) -> 'float':
        """float: 'BendingSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BendingSafetyFactorForFatigue

        if temp is None:
            return 0.0

        return temp

    @property
    def calculated_bending_stress(self) -> 'float':
        """float: 'CalculatedBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.CalculatedBendingStress

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_fatigue(self) -> 'float':
        """float: 'ContactSafetyFactorForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactSafetyFactorForFatigue

        if temp is None:
            return 0.0

        return temp

    @property
    def geometry_factor_j(self) -> 'float':
        """float: 'GeometryFactorJ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GeometryFactorJ

        if temp is None:
            return 0.0

        return temp

    @property
    def life_factor_bending(self) -> 'float':
        """float: 'LifeFactorBending' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorBending

        if temp is None:
            return 0.0

        return temp

    @property
    def life_factor_contact(self) -> 'float':
        """float: 'LifeFactorContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeFactorContact

        if temp is None:
            return 0.0

        return temp

    @property
    def working_bending_stress(self) -> 'float':
        """float: 'WorkingBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingBendingStress

        if temp is None:
            return 0.0

        return temp

    @property
    def working_contact_stress(self) -> 'float':
        """float: 'WorkingContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WorkingContactStress

        if temp is None:
            return 0.0

        return temp
