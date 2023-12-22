﻿"""_2097.py

AngularContactBallBearing
"""


from mastapy.bearings.bearing_designs.rolling import _2102
from mastapy._internal.python_net import python_net_import

_ANGULAR_CONTACT_BALL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'AngularContactBallBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('AngularContactBallBearing',)


class AngularContactBallBearing(_2102.BallBearing):
    """AngularContactBallBearing

    This is a mastapy class.
    """

    TYPE = _ANGULAR_CONTACT_BALL_BEARING

    def __init__(self, instance_to_wrap: 'AngularContactBallBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
