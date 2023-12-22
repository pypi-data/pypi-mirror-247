﻿"""_4670.py

ShaftPerModeResult
"""


from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4663
from mastapy._internal.python_net import python_net_import

_SHAFT_PER_MODE_RESULT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting', 'ShaftPerModeResult')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftPerModeResult',)


class ShaftPerModeResult(_4663.ComponentPerModeResult):
    """ShaftPerModeResult

    This is a mastapy class.
    """

    TYPE = _SHAFT_PER_MODE_RESULT

    def __init__(self, instance_to_wrap: 'ShaftPerModeResult.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def torsional_mode_shape(self) -> 'float':
        """float: 'TorsionalModeShape' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TorsionalModeShape

        if temp is None:
            return 0.0

        return temp
