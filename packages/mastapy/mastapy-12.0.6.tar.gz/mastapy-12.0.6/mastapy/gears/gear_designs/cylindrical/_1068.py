﻿"""_1068.py

StandardRack
"""


from mastapy.gears.gear_designs.cylindrical import _1001
from mastapy._internal.python_net import python_net_import

_STANDARD_RACK = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'StandardRack')


__docformat__ = 'restructuredtext en'
__all__ = ('StandardRack',)


class StandardRack(_1001.CylindricalGearBasicRack):
    """StandardRack

    This is a mastapy class.
    """

    TYPE = _STANDARD_RACK

    def __init__(self, instance_to_wrap: 'StandardRack.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
