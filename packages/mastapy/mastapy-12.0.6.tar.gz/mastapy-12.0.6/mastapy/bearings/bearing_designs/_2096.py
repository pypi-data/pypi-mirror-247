﻿"""_2096.py

NonLinearBearing
"""


from mastapy.bearings.bearing_designs import _2092
from mastapy._internal.python_net import python_net_import

_NON_LINEAR_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns', 'NonLinearBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('NonLinearBearing',)


class NonLinearBearing(_2092.BearingDesign):
    """NonLinearBearing

    This is a mastapy class.
    """

    TYPE = _NON_LINEAR_BEARING

    def __init__(self, instance_to_wrap: 'NonLinearBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
