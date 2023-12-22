﻿"""_6253.py

CVTPulleyDynamicAnalysis
"""


from mastapy.system_model.part_model.couplings import _2543
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6300
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'CVTPulleyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyDynamicAnalysis',)


class CVTPulleyDynamicAnalysis(_6300.PulleyDynamicAnalysis):
    """CVTPulleyDynamicAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_PULLEY_DYNAMIC_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTPulleyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2543.CVTPulley':
        """CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
