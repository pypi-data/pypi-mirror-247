﻿"""_73.py

LinearStiffnessProperties
"""


from mastapy._internal import constructor
from mastapy.nodal_analysis import _46
from mastapy._internal.python_net import python_net_import

_LINEAR_STIFFNESS_PROPERTIES = python_net_import('SMT.MastaAPI.NodalAnalysis', 'LinearStiffnessProperties')


__docformat__ = 'restructuredtext en'
__all__ = ('LinearStiffnessProperties',)


class LinearStiffnessProperties(_46.AbstractLinearConnectionProperties):
    """LinearStiffnessProperties

    This is a mastapy class.
    """

    TYPE = _LINEAR_STIFFNESS_PROPERTIES

    def __init__(self, instance_to_wrap: 'LinearStiffnessProperties.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def axial_stiffness(self) -> 'float':
        """float: 'AxialStiffness' is the original name of this property."""

        temp = self.wrapped.AxialStiffness

        if temp is None:
            return 0.0

        return temp

    @axial_stiffness.setter
    def axial_stiffness(self, value: 'float'):
        self.wrapped.AxialStiffness = float(value) if value is not None else 0.0

    @property
    def radial_stiffness(self) -> 'float':
        """float: 'RadialStiffness' is the original name of this property."""

        temp = self.wrapped.RadialStiffness

        if temp is None:
            return 0.0

        return temp

    @radial_stiffness.setter
    def radial_stiffness(self, value: 'float'):
        self.wrapped.RadialStiffness = float(value) if value is not None else 0.0

    @property
    def tilt_stiffness(self) -> 'float':
        """float: 'TiltStiffness' is the original name of this property."""

        temp = self.wrapped.TiltStiffness

        if temp is None:
            return 0.0

        return temp

    @tilt_stiffness.setter
    def tilt_stiffness(self, value: 'float'):
        self.wrapped.TiltStiffness = float(value) if value is not None else 0.0

    @property
    def torsional_stiffness(self) -> 'float':
        """float: 'TorsionalStiffness' is the original name of this property."""

        temp = self.wrapped.TorsionalStiffness

        if temp is None:
            return 0.0

        return temp

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'float'):
        self.wrapped.TorsionalStiffness = float(value) if value is not None else 0.0
