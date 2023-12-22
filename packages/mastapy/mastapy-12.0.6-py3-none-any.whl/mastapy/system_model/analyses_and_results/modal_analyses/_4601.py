﻿"""_4601.py

ModalAnalysisDrawStyle
"""


from mastapy.system_model.analyses_and_results.dynamic_analyses import _6263
from mastapy._internal.python_net import python_net_import

_MODAL_ANALYSIS_DRAW_STYLE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'ModalAnalysisDrawStyle')


__docformat__ = 'restructuredtext en'
__all__ = ('ModalAnalysisDrawStyle',)


class ModalAnalysisDrawStyle(_6263.DynamicAnalysisDrawStyle):
    """ModalAnalysisDrawStyle

    This is a mastapy class.
    """

    TYPE = _MODAL_ANALYSIS_DRAW_STYLE

    def __init__(self, instance_to_wrap: 'ModalAnalysisDrawStyle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
