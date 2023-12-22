﻿"""_497.py

SafetyFactorOptimisationStepResult
"""


from mastapy.gears.rating import _362
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_SAFETY_FACTOR_OPTIMISATION_STEP_RESULT = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.Optimisation', 'SafetyFactorOptimisationStepResult')


__docformat__ = 'restructuredtext en'
__all__ = ('SafetyFactorOptimisationStepResult',)


class SafetyFactorOptimisationStepResult(_0.APIBase):
    """SafetyFactorOptimisationStepResult

    This is a mastapy class.
    """

    TYPE = _SAFETY_FACTOR_OPTIMISATION_STEP_RESULT

    def __init__(self, instance_to_wrap: 'SafetyFactorOptimisationStepResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def normalised_safety_factors(self) -> '_362.SafetyFactorResults':
        """SafetyFactorResults: 'NormalisedSafetyFactors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NormalisedSafetyFactors

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def safety_factors(self) -> '_362.SafetyFactorResults':
        """SafetyFactorResults: 'SafetyFactors' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SafetyFactors

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
