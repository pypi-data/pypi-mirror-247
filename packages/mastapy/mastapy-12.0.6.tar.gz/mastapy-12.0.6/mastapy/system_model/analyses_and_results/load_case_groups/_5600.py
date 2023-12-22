﻿"""_5600.py

AbstractDesignStateLoadCaseGroup
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.load_case_groups import _5602
from mastapy._internal.python_net import python_net_import

_ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractDesignStateLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractDesignStateLoadCaseGroup',)


class AbstractDesignStateLoadCaseGroup(_5602.AbstractStaticLoadCaseGroup):
    """AbstractDesignStateLoadCaseGroup

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_DESIGN_STATE_LOAD_CASE_GROUP

    def __init__(self, instance_to_wrap: 'AbstractDesignStateLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def two_d_drawing_showing_power_flow(self) -> 'Image':
        """Image: 'TwoDDrawingShowingPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TwoDDrawingShowingPowerFlow

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @property
    def ratio(self) -> 'float':
        """float: 'Ratio' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Ratio

        if temp is None:
            return 0.0

        return temp

    @property
    def target_ratio(self) -> 'float':
        """float: 'TargetRatio' is the original name of this property."""

        temp = self.wrapped.TargetRatio

        if temp is None:
            return 0.0

        return temp

    @target_ratio.setter
    def target_ratio(self, value: 'float'):
        self.wrapped.TargetRatio = float(value) if value is not None else 0.0

    @property
    def target_ratio_tolerance(self) -> 'float':
        """float: 'TargetRatioTolerance' is the original name of this property."""

        temp = self.wrapped.TargetRatioTolerance

        if temp is None:
            return 0.0

        return temp

    @target_ratio_tolerance.setter
    def target_ratio_tolerance(self, value: 'float'):
        self.wrapped.TargetRatioTolerance = float(value) if value is not None else 0.0

    @property
    def target_ratio_tolerance_absolute(self) -> 'float':
        """float: 'TargetRatioToleranceAbsolute' is the original name of this property."""

        temp = self.wrapped.TargetRatioToleranceAbsolute

        if temp is None:
            return 0.0

        return temp

    @target_ratio_tolerance_absolute.setter
    def target_ratio_tolerance_absolute(self, value: 'float'):
        self.wrapped.TargetRatioToleranceAbsolute = float(value) if value is not None else 0.0
