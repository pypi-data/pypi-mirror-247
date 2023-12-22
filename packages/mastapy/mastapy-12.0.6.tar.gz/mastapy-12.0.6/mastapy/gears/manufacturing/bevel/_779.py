﻿"""_779.py

ConicalMeshMicroGeometryConfig
"""


from mastapy.gears.manufacturing.bevel import _780
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MICRO_GEOMETRY_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshMicroGeometryConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshMicroGeometryConfig',)


class ConicalMeshMicroGeometryConfig(_780.ConicalMeshMicroGeometryConfigBase):
    """ConicalMeshMicroGeometryConfig

    This is a mastapy class.
    """

    TYPE = _CONICAL_MESH_MICRO_GEOMETRY_CONFIG

    def __init__(self, instance_to_wrap: 'ConicalMeshMicroGeometryConfig.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
