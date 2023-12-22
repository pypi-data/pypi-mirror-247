﻿"""_828.py

GearContactStiffness
"""


from mastapy.gears.ltca import _840
from mastapy._internal.python_net import python_net_import

_GEAR_CONTACT_STIFFNESS = python_net_import('SMT.MastaAPI.Gears.LTCA', 'GearContactStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('GearContactStiffness',)


class GearContactStiffness(_840.GearStiffness):
    """GearContactStiffness

    This is a mastapy class.
    """

    TYPE = _GEAR_CONTACT_STIFFNESS

    def __init__(self, instance_to_wrap: 'GearContactStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
