﻿"""_2670.py

ConceptCouplingSystemDeflection
"""


from mastapy.system_model.part_model.couplings import _2537
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6772
from mastapy.system_model.analyses_and_results.power_flows import _4009
from mastapy.system_model.analyses_and_results.system_deflections import _2682
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ConceptCouplingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingSystemDeflection',)


class ConceptCouplingSystemDeflection(_2682.CouplingSystemDeflection):
    """ConceptCouplingSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONCEPT_COUPLING_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'ConceptCouplingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2537.ConceptCoupling':
        """ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def assembly_load_case(self) -> '_6772.ConceptCouplingLoadCase':
        """ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def power_flow_results(self) -> '_4009.ConceptCouplingPowerFlow':
        """ConceptCouplingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
