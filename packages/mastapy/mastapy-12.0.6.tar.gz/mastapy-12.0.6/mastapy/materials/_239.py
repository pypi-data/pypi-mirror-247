﻿"""_239.py

BearingMaterial
"""


from mastapy.materials import _263
from mastapy._internal.python_net import python_net_import

_BEARING_MATERIAL = python_net_import('SMT.MastaAPI.Materials', 'BearingMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingMaterial',)


class BearingMaterial(_263.Material):
    """BearingMaterial

    This is a mastapy class.
    """

    TYPE = _BEARING_MATERIAL

    def __init__(self, instance_to_wrap: 'BearingMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
