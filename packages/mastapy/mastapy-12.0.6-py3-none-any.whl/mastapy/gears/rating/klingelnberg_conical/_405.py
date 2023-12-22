﻿"""_405.py

KlingelnbergCycloPalloidConicalGearMeshRating
"""


from mastapy.gears.rating.conical import _532
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.KlingelnbergConical', 'KlingelnbergCycloPalloidConicalGearMeshRating')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidConicalGearMeshRating',)


class KlingelnbergCycloPalloidConicalGearMeshRating(_532.ConicalGearMeshRating):
    """KlingelnbergCycloPalloidConicalGearMeshRating

    This is a mastapy class.
    """

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_RATING

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidConicalGearMeshRating.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
