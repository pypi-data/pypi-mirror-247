﻿"""_1190.py

GearSetFEModel
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _58
from mastapy.gears.fe_model import _1187, _1188
from mastapy import _7489
from mastapy._internal.python_net import python_net_import
from mastapy.gears.analysis import _1221

_TASK_PROGRESS = python_net_import('SMT.MastaAPIUtility', 'TaskProgress')
_GEAR_SET_FE_MODEL = python_net_import('SMT.MastaAPI.Gears.FEModel', 'GearSetFEModel')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetFEModel',)


class GearSetFEModel(_1221.GearSetImplementationDetail):
    """GearSetFEModel

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_FE_MODEL

    def __init__(self, instance_to_wrap: 'GearSetFEModel.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def comment(self) -> 'str':
        """str: 'Comment' is the original name of this property."""

        temp = self.wrapped.Comment

        if temp is None:
            return ''

        return temp

    @comment.setter
    def comment(self, value: 'str'):
        self.wrapped.Comment = str(value) if value is not None else ''

    @property
    def element_order(self) -> '_58.ElementOrder':
        """ElementOrder: 'ElementOrder' is the original name of this property."""

        temp = self.wrapped.ElementOrder

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_58.ElementOrder)(value) if value is not None else None

    @element_order.setter
    def element_order(self, value: '_58.ElementOrder'):
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ElementOrder = value

    @property
    def number_of_coupled_teeth_either_side(self) -> 'int':
        """int: 'NumberOfCoupledTeethEitherSide' is the original name of this property."""

        temp = self.wrapped.NumberOfCoupledTeethEitherSide

        if temp is None:
            return 0

        return temp

    @number_of_coupled_teeth_either_side.setter
    def number_of_coupled_teeth_either_side(self, value: 'int'):
        self.wrapped.NumberOfCoupledTeethEitherSide = int(value) if value is not None else 0

    @property
    def gear_fe_models(self) -> 'List[_1187.GearFEModel]':
        """List[GearFEModel]: 'GearFEModels' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.GearFEModels

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def mesh_fe_models(self) -> 'List[_1188.GearMeshFEModel]':
        """List[GearMeshFEModel]: 'MeshFEModels' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.MeshFEModels

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value

    @property
    def is_ready_for_altca(self) -> 'bool':
        """bool: 'IsReadyForALTCA' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.IsReadyForALTCA

        if temp is None:
            return False

        return temp

    def generate_stiffness_from_fe(self):
        """ 'GenerateStiffnessFromFE' is the original name of this method."""

        self.wrapped.GenerateStiffnessFromFE()

    def generate_stress_influence_coefficients_from_fe(self):
        """ 'GenerateStressInfluenceCoefficientsFromFE' is the original name of this method."""

        self.wrapped.GenerateStressInfluenceCoefficientsFromFE()

    def calculate_stiffness_from_fe(self):
        """ 'CalculateStiffnessFromFE' is the original name of this method."""

        self.wrapped.CalculateStiffnessFromFE()

    def calculate_stiffness_from_fe_with_progress(self, progress: '_7489.TaskProgress'):
        """ 'CalculateStiffnessFromFE' is the original name of this method.

        Args:
            progress (mastapy.TaskProgress)
        """

        self.wrapped.CalculateStiffnessFromFE.Overloads[_TASK_PROGRESS](progress.wrapped if progress else None)
