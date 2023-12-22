﻿"""_6814.py

ElectricMachineHarmonicLoadMotorCADImportOptions
"""


from mastapy.system_model.analyses_and_results.static_loads import _6812
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_HARMONIC_LOAD_MOTOR_CAD_IMPORT_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineHarmonicLoadMotorCADImportOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineHarmonicLoadMotorCADImportOptions',)


class ElectricMachineHarmonicLoadMotorCADImportOptions(_6812.ElectricMachineHarmonicLoadImportOptionsBase):
    """ElectricMachineHarmonicLoadMotorCADImportOptions

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_HARMONIC_LOAD_MOTOR_CAD_IMPORT_OPTIONS

    def __init__(self, instance_to_wrap: 'ElectricMachineHarmonicLoadMotorCADImportOptions.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
