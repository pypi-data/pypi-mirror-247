﻿"""_1917.py

LoadedConceptRadialClearanceBearingResults
"""


from mastapy._internal import constructor
from mastapy.bearings.bearing_results import _1916
from mastapy._internal.python_net import python_net_import

_LOADED_CONCEPT_RADIAL_CLEARANCE_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedConceptRadialClearanceBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedConceptRadialClearanceBearingResults',)


class LoadedConceptRadialClearanceBearingResults(_1916.LoadedConceptClearanceBearingResults):
    """LoadedConceptRadialClearanceBearingResults

    This is a mastapy class.
    """

    TYPE = _LOADED_CONCEPT_RADIAL_CLEARANCE_BEARING_RESULTS

    def __init__(self, instance_to_wrap: 'LoadedConceptRadialClearanceBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def contact_stiffness(self) -> 'float':
        """float: 'ContactStiffness' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ContactStiffness

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_contact_stress(self) -> 'float':
        """float: 'MaximumContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumContactStress

        if temp is None:
            return 0.0

        return temp

    @property
    def surface_penetration_in_middle(self) -> 'float':
        """float: 'SurfacePenetrationInMiddle' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SurfacePenetrationInMiddle

        if temp is None:
            return 0.0

        return temp
