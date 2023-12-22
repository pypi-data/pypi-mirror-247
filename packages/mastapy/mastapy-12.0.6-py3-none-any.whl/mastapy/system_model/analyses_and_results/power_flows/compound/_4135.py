﻿"""_4135.py

ClutchCompoundPowerFlow
"""


from typing import List

from mastapy.system_model.part_model.couplings import _2534
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _4004
from mastapy.system_model.analyses_and_results.power_flows.compound import _4151
from mastapy._internal.python_net import python_net_import

_CLUTCH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'ClutchCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchCompoundPowerFlow',)


class ClutchCompoundPowerFlow(_4151.CouplingCompoundPowerFlow):
    """ClutchCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _CLUTCH_COMPOUND_POWER_FLOW

    def __init__(self, instance_to_wrap: 'ClutchCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2534.Clutch':
        """Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_design(self) -> '_2534.Clutch':
        """Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_4004.ClutchPowerFlow]':
        """List[ClutchPowerFlow]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_4004.ClutchPowerFlow]':
        """List[ClutchPowerFlow]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
