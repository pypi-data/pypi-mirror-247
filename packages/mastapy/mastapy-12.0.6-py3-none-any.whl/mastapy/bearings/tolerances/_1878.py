﻿"""_1878.py

RaceDetail
"""


from mastapy.bearings.tolerances import _1872
from mastapy._internal.python_net import python_net_import

_RACE_DETAIL = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'RaceDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceDetail',)


class RaceDetail(_1872.InterferenceDetail):
    """RaceDetail

    This is a mastapy class.
    """

    TYPE = _RACE_DETAIL

    def __init__(self, instance_to_wrap: 'RaceDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
