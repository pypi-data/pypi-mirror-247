﻿"""_1515.py

ParetoOptimisationOutput
"""


from mastapy._internal import constructor
from mastapy.math_utility.optimisation import _1521
from mastapy._internal.python_net import python_net_import

_PARETO_OPTIMISATION_OUTPUT = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'ParetoOptimisationOutput')


__docformat__ = 'restructuredtext en'
__all__ = ('ParetoOptimisationOutput',)


class ParetoOptimisationOutput(_1521.ParetoOptimistaionVariable):
    """ParetoOptimisationOutput

    This is a mastapy class.
    """

    TYPE = _PARETO_OPTIMISATION_OUTPUT

    def __init__(self, instance_to_wrap: 'ParetoOptimisationOutput.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def percent(self) -> 'float':
        """float: 'Percent' is the original name of this property."""

        temp = self.wrapped.Percent

        if temp is None:
            return 0.0

        return temp

    @percent.setter
    def percent(self, value: 'float'):
        self.wrapped.Percent = float(value) if value is not None else 0.0

    @property
    def exclude_from_dominant_candidates_search(self) -> 'bool':
        """bool: 'ExcludeFromDominantCandidatesSearch' is the original name of this property."""

        temp = self.wrapped.ExcludeFromDominantCandidatesSearch

        if temp is None:
            return False

        return temp

    @exclude_from_dominant_candidates_search.setter
    def exclude_from_dominant_candidates_search(self, value: 'bool'):
        self.wrapped.ExcludeFromDominantCandidatesSearch = bool(value) if value is not None else False

    @property
    def use_original_design_value(self) -> 'bool':
        """bool: 'UseOriginalDesignValue' is the original name of this property."""

        temp = self.wrapped.UseOriginalDesignValue

        if temp is None:
            return False

        return temp

    @use_original_design_value.setter
    def use_original_design_value(self, value: 'bool'):
        self.wrapped.UseOriginalDesignValue = bool(value) if value is not None else False
