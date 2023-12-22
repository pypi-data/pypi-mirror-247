﻿"""_1844.py

BearingSettingsDatabase
"""


from mastapy.utility.databases import _1794
from mastapy.bearings import _1845
from mastapy._internal.python_net import python_net_import

_BEARING_SETTINGS_DATABASE = python_net_import('SMT.MastaAPI.Bearings', 'BearingSettingsDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingSettingsDatabase',)


class BearingSettingsDatabase(_1794.NamedDatabase['_1845.BearingSettingsItem']):
    """BearingSettingsDatabase

    This is a mastapy class.
    """

    TYPE = _BEARING_SETTINGS_DATABASE

    def __init__(self, instance_to_wrap: 'BearingSettingsDatabase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
