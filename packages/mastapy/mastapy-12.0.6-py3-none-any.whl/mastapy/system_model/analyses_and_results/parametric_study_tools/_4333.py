﻿"""_4333.py

ParametricStudyHistogram
"""


from mastapy._internal import constructor
from mastapy.utility.report import _1728
from mastapy._internal.python_net import python_net_import

_PARAMETRIC_STUDY_HISTOGRAM = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'ParametricStudyHistogram')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyHistogram',)


class ParametricStudyHistogram(_1728.CustomReportDefinitionItem):
    """ParametricStudyHistogram

    This is a mastapy class.
    """

    TYPE = _PARAMETRIC_STUDY_HISTOGRAM

    def __init__(self, instance_to_wrap: 'ParametricStudyHistogram.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def height(self) -> 'int':
        """int: 'Height' is the original name of this property."""

        temp = self.wrapped.Height

        if temp is None:
            return 0

        return temp

    @height.setter
    def height(self, value: 'int'):
        self.wrapped.Height = int(value) if value is not None else 0

    @property
    def number_of_bins(self) -> 'int':
        """int: 'NumberOfBins' is the original name of this property."""

        temp = self.wrapped.NumberOfBins

        if temp is None:
            return 0

        return temp

    @number_of_bins.setter
    def number_of_bins(self, value: 'int'):
        self.wrapped.NumberOfBins = int(value) if value is not None else 0

    @property
    def use_bin_range_for_label(self) -> 'bool':
        """bool: 'UseBinRangeForLabel' is the original name of this property."""

        temp = self.wrapped.UseBinRangeForLabel

        if temp is None:
            return False

        return temp

    @use_bin_range_for_label.setter
    def use_bin_range_for_label(self, value: 'bool'):
        self.wrapped.UseBinRangeForLabel = bool(value) if value is not None else False

    @property
    def width(self) -> 'int':
        """int: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return 0

        return temp

    @width.setter
    def width(self, value: 'int'):
        self.wrapped.Width = int(value) if value is not None else 0
