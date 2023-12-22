﻿"""_2796.py

MeshDeflectionResults
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.reporting import _2795
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_MESH_DEFLECTION_RESULTS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting', 'MeshDeflectionResults')


__docformat__ = 'restructuredtext en'
__all__ = ('MeshDeflectionResults',)


class MeshDeflectionResults(_0.APIBase):
    """MeshDeflectionResults

    This is a mastapy class.
    """

    TYPE = _MESH_DEFLECTION_RESULTS

    def __init__(self, instance_to_wrap: 'MeshDeflectionResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def offset(self) -> 'float':
        """float: 'Offset' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Offset

        if temp is None:
            return 0.0

        return temp

    @property
    def total_microgeometry(self) -> 'float':
        """float: 'TotalMicrogeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalMicrogeometry

        if temp is None:
            return 0.0

        return temp

    @property
    def total_transverse_deflection(self) -> 'float':
        """float: 'TotalTransverseDeflection' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalTransverseDeflection

        if temp is None:
            return 0.0

        return temp

    @property
    def total_transverse_deflection_with_microgeometry(self) -> 'float':
        """float: 'TotalTransverseDeflectionWithMicrogeometry' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TotalTransverseDeflectionWithMicrogeometry

        if temp is None:
            return 0.0

        return temp

    @property
    def gears(self) -> 'List[_2795.GearInMeshDeflectionResults]':
        """List[GearInMeshDeflectionResults]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Gears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
