﻿"""_2619.py

CompoundDynamicModelAtAStiffnessAnalysis
"""


from mastapy.system_model.analyses_and_results import _2575
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_MODEL_AT_A_STIFFNESS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicModelAtAStiffnessAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicModelAtAStiffnessAnalysis',)


class CompoundDynamicModelAtAStiffnessAnalysis(_2575.CompoundAnalysis):
    """CompoundDynamicModelAtAStiffnessAnalysis

    This is a mastapy class.
    """

    TYPE = _COMPOUND_DYNAMIC_MODEL_AT_A_STIFFNESS_ANALYSIS

    def __init__(self, instance_to_wrap: 'CompoundDynamicModelAtAStiffnessAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
