﻿"""_858.py

ConicalGearContactStiffness
"""


from mastapy.gears.ltca import _828
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_CONTACT_STIFFNESS = python_net_import('SMT.MastaAPI.Gears.LTCA.Conical', 'ConicalGearContactStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalGearContactStiffness',)


class ConicalGearContactStiffness(_828.GearContactStiffness):
    """ConicalGearContactStiffness

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_CONTACT_STIFFNESS

    def __init__(self, instance_to_wrap: 'ConicalGearContactStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
