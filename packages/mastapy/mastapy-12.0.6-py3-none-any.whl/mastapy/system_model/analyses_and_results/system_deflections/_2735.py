﻿"""_2735.py

OilSealSystemDeflection
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2423
from mastapy.system_model.analyses_and_results.static_loads import _6858
from mastapy.system_model.analyses_and_results.power_flows import _4060
from mastapy.system_model.analyses_and_results.system_deflections import _2679
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'OilSealSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealSystemDeflection',)


class OilSealSystemDeflection(_2679.ConnectorSystemDeflection):
    """OilSealSystemDeflection

    This is a mastapy class.
    """

    TYPE = _OIL_SEAL_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'OilSealSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def reliability_for_oil_seal(self) -> 'float':
        """float: 'ReliabilityForOilSeal' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ReliabilityForOilSeal

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self) -> '_2423.OilSeal':
        """OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_load_case(self) -> '_6858.OilSealLoadCase':
        """OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_4060.OilSealPowerFlow':
        """OilSealPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
