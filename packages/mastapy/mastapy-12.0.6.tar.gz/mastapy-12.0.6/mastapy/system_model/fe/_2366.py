﻿"""_2366.py

RaceBearingFEWithSelection
"""


from mastapy.math_utility import _1466
from mastapy._internal import constructor
from mastapy.system_model.fe import _2364, _2319
from mastapy._internal.python_net import python_net_import

_RACE_BEARING_FE_WITH_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.FE', 'RaceBearingFEWithSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceBearingFEWithSelection',)


class RaceBearingFEWithSelection(_2319.BaseFEWithSelection):
    """RaceBearingFEWithSelection

    This is a mastapy class.
    """

    TYPE = _RACE_BEARING_FE_WITH_SELECTION

    def __init__(self, instance_to_wrap: 'RaceBearingFEWithSelection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def manual_alignment(self) -> '_1466.CoordinateSystemEditor':
        """CoordinateSystemEditor: 'ManualAlignment' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ManualAlignment

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def race_bearing(self) -> '_2364.RaceBearingFE':
        """RaceBearingFE: 'RaceBearing' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RaceBearing

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
