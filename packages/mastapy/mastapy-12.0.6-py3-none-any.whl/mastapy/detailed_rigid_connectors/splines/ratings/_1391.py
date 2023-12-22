﻿"""_1391.py

DIN5466SplineHalfRating
"""


from mastapy.detailed_rigid_connectors.splines.ratings import _1397
from mastapy._internal.python_net import python_net_import

_DIN5466_SPLINE_HALF_RATING = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines.Ratings', 'DIN5466SplineHalfRating')


__docformat__ = 'restructuredtext en'
__all__ = ('DIN5466SplineHalfRating',)


class DIN5466SplineHalfRating(_1397.SplineHalfRating):
    """DIN5466SplineHalfRating

    This is a mastapy class.
    """

    TYPE = _DIN5466_SPLINE_HALF_RATING

    def __init__(self, instance_to_wrap: 'DIN5466SplineHalfRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
