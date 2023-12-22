﻿"""_5705.py

HarmonicAnalysisRootAssemblyExportOptions
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5702
from mastapy.system_model.analyses_and_results import _2611
from mastapy.system_model.part_model import _2431
from mastapy._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_ROOT_ASSEMBLY_EXPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'HarmonicAnalysisRootAssemblyExportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicAnalysisRootAssemblyExportOptions',)


class HarmonicAnalysisRootAssemblyExportOptions(_5702.HarmonicAnalysisExportOptions['_2611.IHaveRootHarmonicAnalysisResults', '_2431.RootAssembly']):
    """HarmonicAnalysisRootAssemblyExportOptions

    This is a mastapy class.
    """

    TYPE = _HARMONIC_ANALYSIS_ROOT_ASSEMBLY_EXPORT_OPTIONS

    def __init__(self, instance_to_wrap: 'HarmonicAnalysisRootAssemblyExportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def include_all_fe_models(self) -> 'bool':
        """bool: 'IncludeAllFEModels' is the original name of this property."""

        temp = self.wrapped.IncludeAllFEModels

        if temp is None:
            return False

        return temp

    @include_all_fe_models.setter
    def include_all_fe_models(self, value: 'bool'):
        self.wrapped.IncludeAllFEModels = bool(value) if value is not None else False

    @property
    def include_all_shafts(self) -> 'bool':
        """bool: 'IncludeAllShafts' is the original name of this property."""

        temp = self.wrapped.IncludeAllShafts

        if temp is None:
            return False

        return temp

    @include_all_shafts.setter
    def include_all_shafts(self, value: 'bool'):
        self.wrapped.IncludeAllShafts = bool(value) if value is not None else False

    @property
    def status_message_for_export(self) -> 'str':
        """str: 'StatusMessageForExport' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.StatusMessageForExport

        if temp is None:
            return ''

        return temp

    def export_to_folder(self, folder_path: 'str') -> 'List[str]':
        """ 'ExportToFolder' is the original name of this method.

        Args:
            folder_path (str)

        Returns:
            List[str]
        """

        folder_path = str(folder_path)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.ExportToFolder(folder_path if folder_path else ''), str)
