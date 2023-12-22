﻿"""_1694.py

TorqueConverterInverseK
"""


from mastapy.utility.units_and_measurements import _1573
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_INVERSE_K = python_net_import('SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements', 'TorqueConverterInverseK')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterInverseK',)


class TorqueConverterInverseK(_1573.MeasurementBase):
    """TorqueConverterInverseK

    This is a mastapy class.
    """

    TYPE = _TORQUE_CONVERTER_INVERSE_K

    def __init__(self, instance_to_wrap: 'TorqueConverterInverseK.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
