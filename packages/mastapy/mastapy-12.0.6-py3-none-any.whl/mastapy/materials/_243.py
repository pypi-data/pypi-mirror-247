﻿"""_243.py

ComponentMaterialDatabase
"""


from mastapy.utility.databases import _1794
from mastapy.materials import _263
from mastapy._internal.python_net import python_net_import

_COMPONENT_MATERIAL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'ComponentMaterialDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentMaterialDatabase',)


class ComponentMaterialDatabase(_1794.NamedDatabase['_263.Material']):
    """ComponentMaterialDatabase

    This is a mastapy class.
    """

    TYPE = _COMPONENT_MATERIAL_DATABASE

    def __init__(self, instance_to_wrap: 'ComponentMaterialDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
