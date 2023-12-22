﻿"""_1134.py

ISO1328AccuracyGraderCommon
"""


from mastapy._internal.implicit import overridable
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical.accuracy_and_tolerances import _1129
from mastapy._internal.python_net import python_net_import

_ISO1328_ACCURACY_GRADER_COMMON = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.AccuracyAndTolerances', 'ISO1328AccuracyGraderCommon')


__docformat__ = 'restructuredtext en'
__all__ = ('ISO1328AccuracyGraderCommon',)


class ISO1328AccuracyGraderCommon(_1129.CylindricalAccuracyGraderWithProfileFormAndSlope):
    """ISO1328AccuracyGraderCommon

    This is a mastapy class.
    """

    TYPE = _ISO1328_ACCURACY_GRADER_COMMON

    def __init__(self, instance_to_wrap: 'ISO1328AccuracyGraderCommon.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def base_pitch_deviation(self) -> 'overridable.Overridable_float':
        """overridable.Overridable_float: 'BasePitchDeviation' is the original name of this property."""

        temp = self.wrapped.BasePitchDeviation

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy_type(overridable.Overridable_float)(temp) if temp is not None else 0.0

    @base_pitch_deviation.setter
    def base_pitch_deviation(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](enclosed_type(value) if value is not None else 0.0, is_overridden)
        self.wrapped.BasePitchDeviation = value
