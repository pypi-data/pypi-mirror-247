﻿"""_518.py

ToothFlankFractureAnalysisContactPointCommon
"""


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating.cylindrical.iso6336 import _521
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_COMMON = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336', 'ToothFlankFractureAnalysisContactPointCommon')


__docformat__ = 'restructuredtext en'
__all__ = ('ToothFlankFractureAnalysisContactPointCommon',)


class ToothFlankFractureAnalysisContactPointCommon(_0.APIBase):
    """ToothFlankFractureAnalysisContactPointCommon

    This is a mastapy class.
    """

    TYPE = _TOOTH_FLANK_FRACTURE_ANALYSIS_CONTACT_POINT_COMMON

    def __init__(self, instance_to_wrap: 'ToothFlankFractureAnalysisContactPointCommon.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def effective_case_depth(self) -> 'float':
        """float: 'EffectiveCaseDepth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.EffectiveCaseDepth

        if temp is None:
            return 0.0

        return temp

    @property
    def half_of_hertzian_contact_width(self) -> 'float':
        """float: 'HalfOfHertzianContactWidth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HalfOfHertzianContactWidth

        if temp is None:
            return 0.0

        return temp

    @property
    def hertzian_contact_stress(self) -> 'float':
        """float: 'HertzianContactStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.HertzianContactStress

        if temp is None:
            return 0.0

        return temp

    @property
    def local_normal_radius_of_relative_curvature(self) -> 'float':
        """float: 'LocalNormalRadiusOfRelativeCurvature' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LocalNormalRadiusOfRelativeCurvature

        if temp is None:
            return 0.0

        return temp

    @property
    def material_factor(self) -> 'float':
        """float: 'MaterialFactor' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialFactor

        if temp is None:
            return 0.0

        return temp

    @property
    def material_factor_constant(self) -> 'float':
        """float: 'MaterialFactorConstant' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaterialFactorConstant

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_material_exposure(self) -> 'float':
        """float: 'MaximumMaterialExposure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumMaterialExposure

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_residual_stress(self) -> 'float':
        """float: 'MaximumResidualStress' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MaximumResidualStress

        if temp is None:
            return 0.0

        return temp

    @property
    def transverse_thickness_at_the_diameter_corresponding_to_the_middle_between_b_and_d(self) -> 'float':
        """float: 'TransverseThicknessAtTheDiameterCorrespondingToTheMiddleBetweenBAndD' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TransverseThicknessAtTheDiameterCorrespondingToTheMiddleBetweenBAndD

        if temp is None:
            return 0.0

        return temp

    @property
    def analysis_point_with_maximum_local_material_exposure(self) -> '_521.ToothFlankFractureAnalysisPoint':
        """ToothFlankFractureAnalysisPoint: 'AnalysisPointWithMaximumLocalMaterialExposure' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AnalysisPointWithMaximumLocalMaterialExposure

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def watch_points(self) -> 'List[_521.ToothFlankFractureAnalysisPoint]':
        """List[ToothFlankFractureAnalysisPoint]: 'WatchPoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.WatchPoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
