﻿"""_1422.py

CycloidalDiscMaterial
"""


from mastapy.materials import _263
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_MATERIAL = python_net_import('SMT.MastaAPI.Cycloidal', 'CycloidalDiscMaterial')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscMaterial',)


class CycloidalDiscMaterial(_263.Material):
    """CycloidalDiscMaterial

    This is a mastapy class.
    """

    TYPE = _CYCLOIDAL_DISC_MATERIAL

    def __init__(self, instance_to_wrap: 'CycloidalDiscMaterial.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
