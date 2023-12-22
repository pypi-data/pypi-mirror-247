﻿"""_1772.py

OrderWithRadius
"""


from mastapy._internal import constructor
from mastapy.utility.modal_analysis.gears import _1770
from mastapy._internal.python_net import python_net_import

_ORDER_WITH_RADIUS = python_net_import('SMT.MastaAPI.Utility.ModalAnalysis.Gears', 'OrderWithRadius')


__docformat__ = 'restructuredtext en'
__all__ = ('OrderWithRadius',)


class OrderWithRadius(_1770.OrderForTE):
    """OrderWithRadius

    This is a mastapy class.
    """

    TYPE = _ORDER_WITH_RADIUS

    def __init__(self, instance_to_wrap: 'OrderWithRadius.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def radius(self) -> 'float':
        """float: 'Radius' is the original name of this property."""

        temp = self.wrapped.Radius

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    def radius(self, value: 'float'):
        self.wrapped.Radius = float(value) if value is not None else 0.0
