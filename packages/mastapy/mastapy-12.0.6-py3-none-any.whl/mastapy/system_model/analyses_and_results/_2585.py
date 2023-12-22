﻿"""_2585.py

DynamicModelForModalAnalysis
"""


from mastapy.system_model.analyses_and_results import _2576
from mastapy._internal.python_net import python_net_import

_DYNAMIC_MODEL_FOR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'DynamicModelForModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DynamicModelForModalAnalysis',)


class DynamicModelForModalAnalysis(_2576.SingleAnalysis):
    """DynamicModelForModalAnalysis

    This is a mastapy class.
    """

    TYPE = _DYNAMIC_MODEL_FOR_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'DynamicModelForModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
