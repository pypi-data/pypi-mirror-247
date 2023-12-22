﻿"""_3.py

PythonUtility
"""


from mastapy._internal import constructor
from mastapy._internal.class_property import classproperty
from mastapy._internal.python_net import python_net_import

_PYTHON_UTILITY = python_net_import('SMT.MastaAPI', 'PythonUtility')


__docformat__ = 'restructuredtext en'
__all__ = ('PythonUtility',)


class PythonUtility:
    """PythonUtility

    This is a mastapy class.
    """

    TYPE = _PYTHON_UTILITY

    def __init__(self, instance_to_wrap: 'PythonUtility.TYPE'):
        self.wrapped = instance_to_wrap
        if not hasattr(self.wrapped, 'reference_count'):
            self.wrapped.reference_count = 0
        self.wrapped.reference_count += 1

    @classproperty
    def python_install_directory(cls) -> 'str':
        """str: 'PythonInstallDirectory' is the original name of this property."""

        temp = PythonUtility.TYPE.PythonInstallDirectory

        if temp is None:
            return ''

        return temp

    @python_install_directory.setter
    def python_install_directory(cls, value: 'str'):
        PythonUtility.TYPE.PythonInstallDirectory = str(value) if value is not None else ''
