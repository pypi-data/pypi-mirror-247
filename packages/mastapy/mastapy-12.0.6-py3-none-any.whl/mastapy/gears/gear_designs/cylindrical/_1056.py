﻿"""_1056.py

NamedPlanetAssemblyIndex
"""


from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_NAMED_PLANET_ASSEMBLY_INDEX = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'NamedPlanetAssemblyIndex')


__docformat__ = 'restructuredtext en'
__all__ = ('NamedPlanetAssemblyIndex',)


class NamedPlanetAssemblyIndex(_0.APIBase):
    """NamedPlanetAssemblyIndex

    This is a mastapy class.
    """

    TYPE = _NAMED_PLANET_ASSEMBLY_INDEX

    def __init__(self, instance_to_wrap: 'NamedPlanetAssemblyIndex.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planet_assembly_index(self) -> 'float':
        """float: 'PlanetAssemblyIndex' is the original name of this property."""

        temp = self.wrapped.PlanetAssemblyIndex

        if temp is None:
            return 0.0

        return temp

    @planet_assembly_index.setter
    def planet_assembly_index(self, value: 'float'):
        self.wrapped.PlanetAssemblyIndex = float(value) if value is not None else 0.0
