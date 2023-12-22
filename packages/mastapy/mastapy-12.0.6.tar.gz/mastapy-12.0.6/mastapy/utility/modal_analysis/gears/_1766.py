﻿"""_1766.py

GearOrderForTE
"""


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.utility.modal_analysis.gears import _1767, _1770, _1772
from mastapy._internal.python_net import python_net_import

_GEAR_ORDER_FOR_TE = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'GearOrderForTE')


__docformat__ = 'restructuredtext en'
__all__ = ('GearOrderForTE',)


class GearOrderForTE(_1772.OrderWithRadius):
    """GearOrderForTE

    This is a mastapy class.
    """

    TYPE = _GEAR_ORDER_FOR_TE

    def __init__(self, instance_to_wrap: 'GearOrderForTE.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_teeth(self) -> 'int':
        """int: 'NumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.NumberOfTeeth

        if temp is None:
            return 0

        return temp

    @property
    def position(self) -> '_1767.GearPositions':
        """GearPositions: 'Position' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Position

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp)
        return constructor.new_from_mastapy_type(_1767.GearPositions)(value) if value is not None else None

    @property
    def additional_orders_and_harmonics(self) -> 'List[_1770.OrderForTE]':
        """List[OrderForTE]: 'AdditionalOrdersAndHarmonics' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdditionalOrdersAndHarmonics

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
