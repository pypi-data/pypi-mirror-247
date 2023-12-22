﻿"""_2415.py

InnerBearingRaceMountingOptions
"""


from mastapy.system_model.part_model import _2398
from mastapy._internal.python_net import python_net_import

_INNER_BEARING_RACE_MOUNTING_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'InnerBearingRaceMountingOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('InnerBearingRaceMountingOptions',)


class InnerBearingRaceMountingOptions(_2398.BearingRaceMountingOptions):
    """InnerBearingRaceMountingOptions

    This is a mastapy class.
    """

    TYPE = _INNER_BEARING_RACE_MOUNTING_OPTIONS

    def __init__(self, instance_to_wrap: 'InnerBearingRaceMountingOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
