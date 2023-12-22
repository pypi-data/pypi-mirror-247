﻿"""_4473.py

PlanetaryConnectionCompoundParametricStudyTool
"""


from typing import List

from mastapy.system_model.connections_and_sockets import _2246
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4344
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4487
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'PlanetaryConnectionCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundParametricStudyTool',)


class PlanetaryConnectionCompoundParametricStudyTool(_4487.ShaftToMountableComponentConnectionCompoundParametricStudyTool):
    """PlanetaryConnectionCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _PLANETARY_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2246.PlanetaryConnection':
        """PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_design(self) -> '_2246.PlanetaryConnection':
        """PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def connection_analysis_cases_ready(self) -> 'List[_4344.PlanetaryConnectionParametricStudyTool]':
        """List[PlanetaryConnectionParametricStudyTool]: 'ConnectionAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def connection_analysis_cases(self) -> 'List[_4344.PlanetaryConnectionParametricStudyTool]':
        """List[PlanetaryConnectionParametricStudyTool]: 'ConnectionAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
