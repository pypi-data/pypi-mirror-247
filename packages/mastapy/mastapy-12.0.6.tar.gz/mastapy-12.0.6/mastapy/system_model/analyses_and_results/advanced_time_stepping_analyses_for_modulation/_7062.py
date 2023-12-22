﻿"""_7062.py

TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation
"""


from mastapy.system_model.part_model.couplings import _2566
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6907
from mastapy.system_model.analyses_and_results.system_deflections import _2782
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6980
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation',)


class TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation(_6980.CouplingHalfAdvancedTimeSteppingAnalysisForModulation):
    """TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_TURBINE_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2566.TorqueConverterTurbine':
        """TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6907.TorqueConverterTurbineLoadCase':
        """TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def system_deflection_results(self) -> '_2782.TorqueConverterTurbineSystemDeflection':
        """TorqueConverterTurbineSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
