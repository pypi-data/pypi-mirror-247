﻿"""_600.py

RawMaterialDatabase
"""


from mastapy.utility.databases import _1794
from mastapy.gears.materials import _599
from mastapy._internal.python_net import python_net_import

_RAW_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Gears.Materials', 'RawMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('RawMaterialDatabase',)


class RawMaterialDatabase(_1794.NamedDatabase['_599.RawMaterial']):
    """RawMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _RAW_MATERIAL_DATABASE

    def __init__(self, instance_to_wrap: 'RawMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
