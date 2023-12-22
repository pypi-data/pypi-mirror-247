﻿"""_6982.py

CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation
"""


from mastapy.system_model.connections_and_sockets import _2232
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2683
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6950
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation',)


class CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation(_6950.BeltConnectionAdvancedTimeSteppingAnalysisForModulation):
    """CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _CVT_BELT_CONNECTION_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2232.CVTBeltConnection':
        """CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2683.CVTBeltConnectionSystemDeflection':
        """CVTBeltConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
