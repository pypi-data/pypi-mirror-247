﻿"""_2621.py

CompoundDynamicModelForModalAnalysis
"""


from mastapy.system_model.analyses_and_results import _2575
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_MODEL_FOR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicModelForModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicModelForModalAnalysis',)


class CompoundDynamicModelForModalAnalysis(_2575.CompoundAnalysis):
    """CompoundDynamicModelForModalAnalysis

    This is a mastapy class.
    """

    TYPE = _COMPOUND_DYNAMIC_MODEL_FOR_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'CompoundDynamicModelForModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
