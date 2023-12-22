﻿"""_565.py

LeadModification
"""


from typing import Optional

from mastapy._internal import constructor
from mastapy.math_utility import _1501
from mastapy.gears.micro_geometry import _572
from mastapy._internal.python_net import python_net_import

_LEAD_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'LeadModification')


__docformat__ = 'restructuredtext en'
__all__ = ('LeadModification',)


class LeadModification(_572.Modification):
    """LeadModification

    This is a mastapy class.
    """

    TYPE = _LEAD_MODIFICATION

    def __init__(self, instance_to_wrap: 'LeadModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def crowning_relief(self) -> 'float':
        """float: 'CrowningRelief' is the original name of this property."""

        temp = self.wrapped.CrowningRelief

        if temp is None:
            return 0.0

        return temp

    @crowning_relief.setter
    def crowning_relief(self, value: 'float'):
        self.wrapped.CrowningRelief = float(value) if value is not None else 0.0

    @property
    def evaluation_left_limit_factor(self) -> 'float':
        """float: 'EvaluationLeftLimitFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationLeftLimitFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_left_limit_factor.setter
    def evaluation_left_limit_factor(self, value: 'float'):
        self.wrapped.EvaluationLeftLimitFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_linear_left_relief_factor(self) -> 'float':
        """float: 'EvaluationOfLinearLeftReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearLeftReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_left_relief_factor.setter
    def evaluation_of_linear_left_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfLinearLeftReliefFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_linear_right_relief_factor(self) -> 'float':
        """float: 'EvaluationOfLinearRightReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearRightReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_right_relief_factor.setter
    def evaluation_of_linear_right_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfLinearRightReliefFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_linear_side_relief_factor(self) -> 'Optional[float]':
        """Optional[float]: 'EvaluationOfLinearSideReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfLinearSideReliefFactor

        if temp is None:
            return None

        return temp

    @evaluation_of_linear_side_relief_factor.setter
    def evaluation_of_linear_side_relief_factor(self, value: 'Optional[float]'):
        self.wrapped.EvaluationOfLinearSideReliefFactor = value

    @property
    def evaluation_of_parabolic_left_relief_factor(self) -> 'float':
        """float: 'EvaluationOfParabolicLeftReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicLeftReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_left_relief_factor.setter
    def evaluation_of_parabolic_left_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicLeftReliefFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_parabolic_right_relief_factor(self) -> 'float':
        """float: 'EvaluationOfParabolicRightReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicRightReliefFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_right_relief_factor.setter
    def evaluation_of_parabolic_right_relief_factor(self, value: 'float'):
        self.wrapped.EvaluationOfParabolicRightReliefFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_of_parabolic_side_relief_factor(self) -> 'Optional[float]':
        """Optional[float]: 'EvaluationOfParabolicSideReliefFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationOfParabolicSideReliefFactor

        if temp is None:
            return None

        return temp

    @evaluation_of_parabolic_side_relief_factor.setter
    def evaluation_of_parabolic_side_relief_factor(self, value: 'Optional[float]'):
        self.wrapped.EvaluationOfParabolicSideReliefFactor = value

    @property
    def evaluation_right_limit_factor(self) -> 'float':
        """float: 'EvaluationRightLimitFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationRightLimitFactor

        if temp is None:
            return 0.0

        return temp

    @evaluation_right_limit_factor.setter
    def evaluation_right_limit_factor(self, value: 'float'):
        self.wrapped.EvaluationRightLimitFactor = float(value) if value is not None else 0.0

    @property
    def evaluation_side_limit_factor(self) -> 'Optional[float]':
        """Optional[float]: 'EvaluationSideLimitFactor' is the original name of this property."""

        temp = self.wrapped.EvaluationSideLimitFactor

        if temp is None:
            return None

        return temp

    @evaluation_side_limit_factor.setter
    def evaluation_side_limit_factor(self, value: 'Optional[float]'):
        self.wrapped.EvaluationSideLimitFactor = value

    @property
    def linear_left_relief(self) -> 'float':
        """float: 'LinearLeftRelief' is the original name of this property."""

        temp = self.wrapped.LinearLeftRelief

        if temp is None:
            return 0.0

        return temp

    @linear_left_relief.setter
    def linear_left_relief(self, value: 'float'):
        self.wrapped.LinearLeftRelief = float(value) if value is not None else 0.0

    @property
    def linear_relief(self) -> 'float':
        """float: 'LinearRelief' is the original name of this property."""

        temp = self.wrapped.LinearRelief

        if temp is None:
            return 0.0

        return temp

    @linear_relief.setter
    def linear_relief(self, value: 'float'):
        self.wrapped.LinearRelief = float(value) if value is not None else 0.0

    @property
    def linear_right_relief(self) -> 'float':
        """float: 'LinearRightRelief' is the original name of this property."""

        temp = self.wrapped.LinearRightRelief

        if temp is None:
            return 0.0

        return temp

    @linear_right_relief.setter
    def linear_right_relief(self, value: 'float'):
        self.wrapped.LinearRightRelief = float(value) if value is not None else 0.0

    @property
    def linear_side_relief(self) -> 'Optional[float]':
        """Optional[float]: 'LinearSideRelief' is the original name of this property."""

        temp = self.wrapped.LinearSideRelief

        if temp is None:
            return None

        return temp

    @linear_side_relief.setter
    def linear_side_relief(self, value: 'Optional[float]'):
        self.wrapped.LinearSideRelief = value

    @property
    def measured_data(self) -> '_1501.Vector2DListAccessor':
        """Vector2DListAccessor: 'MeasuredData' is the original name of this property."""

        temp = self.wrapped.MeasuredData

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @measured_data.setter
    def measured_data(self, value: '_1501.Vector2DListAccessor'):
        self.wrapped.MeasuredData = value

    @property
    def parabolic_left_relief(self) -> 'float':
        """float: 'ParabolicLeftRelief' is the original name of this property."""

        temp = self.wrapped.ParabolicLeftRelief

        if temp is None:
            return 0.0

        return temp

    @parabolic_left_relief.setter
    def parabolic_left_relief(self, value: 'float'):
        self.wrapped.ParabolicLeftRelief = float(value) if value is not None else 0.0

    @property
    def parabolic_right_relief(self) -> 'float':
        """float: 'ParabolicRightRelief' is the original name of this property."""

        temp = self.wrapped.ParabolicRightRelief

        if temp is None:
            return 0.0

        return temp

    @parabolic_right_relief.setter
    def parabolic_right_relief(self, value: 'float'):
        self.wrapped.ParabolicRightRelief = float(value) if value is not None else 0.0

    @property
    def parabolic_side_relief(self) -> 'Optional[float]':
        """Optional[float]: 'ParabolicSideRelief' is the original name of this property."""

        temp = self.wrapped.ParabolicSideRelief

        if temp is None:
            return None

        return temp

    @parabolic_side_relief.setter
    def parabolic_side_relief(self, value: 'Optional[float]'):
        self.wrapped.ParabolicSideRelief = value

    @property
    def start_of_linear_left_relief_factor(self) -> 'float':
        """float: 'StartOfLinearLeftReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfLinearLeftReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_left_relief_factor.setter
    def start_of_linear_left_relief_factor(self, value: 'float'):
        self.wrapped.StartOfLinearLeftReliefFactor = float(value) if value is not None else 0.0

    @property
    def start_of_linear_right_relief_factor(self) -> 'float':
        """float: 'StartOfLinearRightReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfLinearRightReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_right_relief_factor.setter
    def start_of_linear_right_relief_factor(self, value: 'float'):
        self.wrapped.StartOfLinearRightReliefFactor = float(value) if value is not None else 0.0

    @property
    def start_of_linear_side_relief_factor(self) -> 'Optional[float]':
        """Optional[float]: 'StartOfLinearSideReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfLinearSideReliefFactor

        if temp is None:
            return None

        return temp

    @start_of_linear_side_relief_factor.setter
    def start_of_linear_side_relief_factor(self, value: 'Optional[float]'):
        self.wrapped.StartOfLinearSideReliefFactor = value

    @property
    def start_of_parabolic_left_relief_factor(self) -> 'float':
        """float: 'StartOfParabolicLeftReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicLeftReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_left_relief_factor.setter
    def start_of_parabolic_left_relief_factor(self, value: 'float'):
        self.wrapped.StartOfParabolicLeftReliefFactor = float(value) if value is not None else 0.0

    @property
    def start_of_parabolic_right_relief_factor(self) -> 'float':
        """float: 'StartOfParabolicRightReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicRightReliefFactor

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_right_relief_factor.setter
    def start_of_parabolic_right_relief_factor(self, value: 'float'):
        self.wrapped.StartOfParabolicRightReliefFactor = float(value) if value is not None else 0.0

    @property
    def start_of_parabolic_side_relief_factor(self) -> 'Optional[float]':
        """Optional[float]: 'StartOfParabolicSideReliefFactor' is the original name of this property."""

        temp = self.wrapped.StartOfParabolicSideReliefFactor

        if temp is None:
            return None

        return temp

    @start_of_parabolic_side_relief_factor.setter
    def start_of_parabolic_side_relief_factor(self, value: 'Optional[float]'):
        self.wrapped.StartOfParabolicSideReliefFactor = value

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
