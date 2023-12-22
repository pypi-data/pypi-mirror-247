﻿"""_262.py

LubricationDetailDatabase
"""


from mastapy.utility.databases import _1794
from mastapy.materials import _261
from mastapy._internal.python_net import python_net_import

_LUBRICATION_DETAIL_DATABASE = python_net_import('SMT.MastaAPI.Materials', 'LubricationDetailDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('LubricationDetailDatabase',)


class LubricationDetailDatabase(_1794.NamedDatabase['_261.LubricationDetail']):
    """LubricationDetailDatabase

    This is a mastapy class.
    """

    TYPE = _LUBRICATION_DETAIL_DATABASE

    def __init__(self, instance_to_wrap: 'LubricationDetailDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
