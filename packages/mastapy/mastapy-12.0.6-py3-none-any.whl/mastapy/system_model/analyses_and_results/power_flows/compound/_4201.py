﻿"""_4201.py

PowerLoadCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model import _2429
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4071
from mastapy.system_model.analyses_and_results.power_flows.compound import _4236
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PowerLoadCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundPowerFlow',)


class PowerLoadCompoundPowerFlow(_4236.VirtualComponentCompoundPowerFlow):
    """PowerLoadCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _POWER_LOAD_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2429.PowerLoad':
        """PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4071.PowerLoadPowerFlow]':
        """List[PowerLoadPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4071.PowerLoadPowerFlow]':
        """List[PowerLoadPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
