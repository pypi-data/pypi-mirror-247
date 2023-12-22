﻿"""_2069.py

ISOTS162812008Results
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _2068
from mastapy._internal.python_net import python_net_import

_ISOTS162812008_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults', 'ISOTS162812008Results')


__docformat__ = 'restructuredtext en'
__all__ = ('ISOTS162812008Results',)


class ISOTS162812008Results(_2068.ISOResults):
    """ISOTS162812008Results

    This is a mastapy class.
    """

    TYPE = _ISOTS162812008_RESULTS

    def __init__(self, instance_to_wrap: 'ISOTS162812008Results.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def basic_reference_rating_life_cycles(self) -> 'float':
        """float: 'BasicReferenceRatingLifeCycles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicReferenceRatingLifeCycles

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_reference_rating_life_damage(self) -> 'float':
        """float: 'BasicReferenceRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicReferenceRatingLifeDamage

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_reference_rating_life_damage_rate(self) -> 'float':
        """float: 'BasicReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicReferenceRatingLifeDamageRate

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_reference_rating_life_reliability(self) -> 'float':
        """float: 'BasicReferenceRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicReferenceRatingLifeReliability

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_reference_rating_life_safety_factor(self) -> 'float':
        """float: 'BasicReferenceRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicReferenceRatingLifeSafetyFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_reference_rating_life_time(self) -> 'float':
        """float: 'BasicReferenceRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicReferenceRatingLifeTime

        if temp is None:
            return 0.0

        return temp

    @property
    def basic_reference_rating_life_unreliability(self) -> 'float':
        """float: 'BasicReferenceRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.BasicReferenceRatingLifeUnreliability

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_equivalent_load_dynamic_capacity_ratio(self) -> 'float':
        """float: 'DynamicEquivalentLoadDynamicCapacityRatio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicEquivalentLoadDynamicCapacityRatio

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_equivalent_reference_load(self) -> 'float':
        """float: 'DynamicEquivalentReferenceLoad' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DynamicEquivalentReferenceLoad

        if temp is None:
            return 0.0

        return temp

    @property
    def life_modification_factor_for_systems_approach(self) -> 'float':
        """float: 'LifeModificationFactorForSystemsApproach' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LifeModificationFactorForSystemsApproach

        if temp is None:
            return 0.0

        return temp

    @property
    def load_for_the_basic_dynamic_load_rating_of_the_inner_ring_or_shaft_washer(self) -> 'float':
        """float: 'LoadForTheBasicDynamicLoadRatingOfTheInnerRingOrShaftWasher' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadForTheBasicDynamicLoadRatingOfTheInnerRingOrShaftWasher

        if temp is None:
            return 0.0

        return temp

    @property
    def load_for_the_basic_dynamic_load_rating_of_the_outer_ring_or_housing_washer(self) -> 'float':
        """float: 'LoadForTheBasicDynamicLoadRatingOfTheOuterRingOrHousingWasher' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LoadForTheBasicDynamicLoadRatingOfTheOuterRingOrHousingWasher

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_reference_rating_life_cycles(self) -> 'float':
        """float: 'ModifiedReferenceRatingLifeCycles' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedReferenceRatingLifeCycles

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_reference_rating_life_damage(self) -> 'float':
        """float: 'ModifiedReferenceRatingLifeDamage' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedReferenceRatingLifeDamage

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_reference_rating_life_damage_rate(self) -> 'float':
        """float: 'ModifiedReferenceRatingLifeDamageRate' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedReferenceRatingLifeDamageRate

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_reference_rating_life_reliability(self) -> 'float':
        """float: 'ModifiedReferenceRatingLifeReliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedReferenceRatingLifeReliability

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_reference_rating_life_safety_factor(self) -> 'float':
        """float: 'ModifiedReferenceRatingLifeSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedReferenceRatingLifeSafetyFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_reference_rating_life_time(self) -> 'float':
        """float: 'ModifiedReferenceRatingLifeTime' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedReferenceRatingLifeTime

        if temp is None:
            return 0.0

        return temp

    @property
    def modified_reference_rating_life_unreliability(self) -> 'float':
        """float: 'ModifiedReferenceRatingLifeUnreliability' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ModifiedReferenceRatingLifeUnreliability

        if temp is None:
            return 0.0

        return temp
