﻿"""_1218.py

GearSetImplementationAnalysis
"""


from typing import Optional

from mastapy._internal import constructor
from mastapy import _7489
from mastapy.gears.analysis import _1219
from mastapy._internal.python_net import python_net_import

_GEAR_SET_IMPLEMENTATION_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearSetImplementationAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetImplementationAnalysis',)


class GearSetImplementationAnalysis(_1219.GearSetImplementationAnalysisAbstract):
    """GearSetImplementationAnalysis

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_IMPLEMENTATION_ANALYSIS

    def __init__(self, instance_to_wrap: 'GearSetImplementationAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def valid_results_ready(self) -> 'bool':
        """bool: 'ValidResultsReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ValidResultsReady

        if temp is None:
            return False

        return temp

    def perform_analysis(self, run_all_planetary_meshes: Optional['bool'] = True):
        """ 'PerformAnalysis' is the original name of this method.

        Args:
            run_all_planetary_meshes (bool, optional)
        """

        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        self.wrapped.PerformAnalysis(run_all_planetary_meshes if run_all_planetary_meshes else False)

    def perform_analysis_with_progress(self, run_all_planetary_meshes: 'bool', progress: '_7489.TaskProgress'):
        """ 'PerformAnalysisWithProgress' is the original name of this method.

        Args:
            run_all_planetary_meshes (bool)
            progress (mastapy.TaskProgress)
        """

        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        self.wrapped.PerformAnalysisWithProgress(run_all_planetary_meshes if run_all_planetary_meshes else False, progress.wrapped if progress else None)

    def results_ready_for(self, run_all_planetary_meshes: Optional['bool'] = True) -> 'bool':
        """ 'ResultsReadyFor' is the original name of this method.

        Args:
            run_all_planetary_meshes (bool, optional)

        Returns:
            bool
        """

        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        method_result = self.wrapped.ResultsReadyFor(run_all_planetary_meshes if run_all_planetary_meshes else False)
        return method_result
