﻿"""_4561.py

CVTModalAnalysis
"""


from mastapy.system_model.part_model.couplings import _2542
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2685
from mastapy.system_model.analyses_and_results.modal_analyses import _4529
from mastapy._internal.python_net import python_net_import

_CVT_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CVTModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTModalAnalysis',)


class CVTModalAnalysis(_4529.BeltDriveModalAnalysis):
    """CVTModalAnalysis

    This is a mastapy class.
    """

    TYPE = _CVT_MODAL_ANALYSIS

    def __init__(self, instance_to_wrap: 'CVTModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2542.CVT':
        """CVT: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2685.CVTSystemDeflection':
        """CVTSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
