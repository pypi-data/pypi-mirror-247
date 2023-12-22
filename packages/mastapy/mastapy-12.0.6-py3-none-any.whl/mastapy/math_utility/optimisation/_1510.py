﻿"""_1510.py

OptimisationHistory
"""


from typing import List

from mastapy.math_utility.optimisation import _1512
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_OPTIMISATION_HISTORY = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'OptimisationHistory')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimisationHistory',)


class OptimisationHistory(_0.APIBase):
    """OptimisationHistory

    This is a mastapy class.
    """

    TYPE = _OPTIMISATION_HISTORY

    def __init__(self, instance_to_wrap: 'OptimisationHistory.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def input_history(self) -> 'List[_1512.OptimizationVariable]':
        """List[OptimizationVariable]: 'InputHistory' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputHistory

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def input_names(self) -> 'List[str]':
        """List[str]: 'InputNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.InputNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    @property
    def target_history(self) -> 'List[_1512.OptimizationVariable]':
        """List[OptimizationVariable]: 'TargetHistory' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TargetHistory

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def target_names(self) -> 'List[str]':
        """List[str]: 'TargetNames' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TargetNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)
        return value

    def add_input_history(self, value: '_1512.OptimizationVariable'):
        """ 'AddInputHistory' is the original name of this method.

        Args:
            value (mastapy.math_utility.optimisation.OptimizationVariable)
        """

        self.wrapped.AddInputHistory(value.wrapped if value else None)

    def add_target_history(self, value: '_1512.OptimizationVariable'):
        """ 'AddTargetHistory' is the original name of this method.

        Args:
            value (mastapy.math_utility.optimisation.OptimizationVariable)
        """

        self.wrapped.AddTargetHistory(value.wrapped if value else None)
