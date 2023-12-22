﻿"""_1838.py

BearingLoadCaseResultsForPst
"""


from mastapy._internal import constructor
from mastapy.bearings import _1839
from mastapy._internal.python_net import python_net_import

_BEARING_LOAD_CASE_RESULTS_FOR_PST = python_net_import('SMT.MastaAPI.Bearings', 'BearingLoadCaseResultsForPst')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingLoadCaseResultsForPst',)


class BearingLoadCaseResultsForPst(_1839.BearingLoadCaseResultsLightweight):
    """BearingLoadCaseResultsForPst

    This is a mastapy class.
    """

    TYPE = _BEARING_LOAD_CASE_RESULTS_FOR_PST

    def __init__(self, instance_to_wrap: 'BearingLoadCaseResultsForPst.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def relative_misalignment(self) -> 'float':
        """float: 'RelativeMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RelativeMisalignment

        if temp is None:
            return 0.0

        return temp
