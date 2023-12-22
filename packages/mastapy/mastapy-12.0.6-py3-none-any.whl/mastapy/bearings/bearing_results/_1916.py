﻿"""_1916.py

LoadedConceptClearanceBearingResults
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results import _1921
from mastapy._internal.python_net import python_net_import

_LOADED_CONCEPT_CLEARANCE_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedConceptClearanceBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedConceptClearanceBearingResults',)


class LoadedConceptClearanceBearingResults(_1921.LoadedNonLinearBearingResults):
    """LoadedConceptClearanceBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_CONCEPT_CLEARANCE_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedConceptClearanceBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_in_contact(self) -> 'bool':
        """bool: 'IsInContact' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsInContact

        if temp is None:
            return False

        return temp

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
