﻿"""_4293.py

CylindricalPlanetGearParametricStudyTool
"""


from mastapy.system_model.part_model.gears import _2483
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4291
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CylindricalPlanetGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearParametricStudyTool',)


class CylindricalPlanetGearParametricStudyTool(_4291.CylindricalGearParametricStudyTool):
    """CylindricalPlanetGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_PLANET_GEAR_PARAMETRIC_STUDY_TOOL

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2483.CylindricalPlanetGear':
        """CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
