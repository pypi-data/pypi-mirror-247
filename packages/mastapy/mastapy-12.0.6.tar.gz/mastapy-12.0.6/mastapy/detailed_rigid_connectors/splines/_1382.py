﻿"""_1382.py

SplineMaterial
"""


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.detailed_rigid_connectors.splines import _1364
from mastapy.materials import _263
from mastapy._internal.python_net import python_net_import

_SPLINE_MATERIAL = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'SplineMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('SplineMaterial',)


class SplineMaterial(_263.Material):
    """SplineMaterial

    This is a mastapy class.
    """

    TYPE = _SPLINE_MATERIAL

    def __init__(self, instance_to_wrap: 'SplineMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def core_hardness_h_rc(self) -> 'float':
        """float: 'CoreHardnessHRc' is the original name of this property."""

        temp = self.wrapped.CoreHardnessHRc

        if temp is None:
            return 0.0

        return temp

    @core_hardness_h_rc.setter
    def core_hardness_h_rc(self, value: 'float'):
        self.wrapped.CoreHardnessHRc = float(value) if value is not None else 0.0

    @property
    def heat_treatment_type(self) -> '_1364.HeatTreatmentTypes':
        """HeatTreatmentTypes: 'HeatTreatmentType' is the original name of this property."""

        temp = self.wrapped.HeatTreatmentType

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1364.HeatTreatmentTypes)(value) if value is not None else None

    @heat_treatment_type.setter
    def heat_treatment_type(self, value: '_1364.HeatTreatmentTypes'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HeatTreatmentType = value
