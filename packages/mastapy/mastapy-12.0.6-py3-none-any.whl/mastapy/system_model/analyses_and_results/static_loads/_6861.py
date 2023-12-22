﻿"""_6861.py

PartToPartShearCouplingConnectionLoadCase
"""


from mastapy.system_model.connections_and_sockets.couplings import _2307
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6783
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'PartToPartShearCouplingConnectionLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingConnectionLoadCase',)


class PartToPartShearCouplingConnectionLoadCase(_6783.CouplingConnectionLoadCase):
    """PartToPartShearCouplingConnectionLoadCase

    This is a mastapy class.
    """

    TYPE = _PART_TO_PART_SHEAR_COUPLING_CONNECTION_LOAD_CASE

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingConnectionLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2307.PartToPartShearCouplingConnection':
        """PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
