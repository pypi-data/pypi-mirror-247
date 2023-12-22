﻿"""_5674.py

ElectricMachinePeriodicExcitationDetail
"""


from mastapy.system_model.analyses_and_results.harmonic_analyses import _5728
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ElectricMachinePeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachinePeriodicExcitationDetail',)


class ElectricMachinePeriodicExcitationDetail(_5728.PeriodicExcitationWithReferenceShaft):
    """ElectricMachinePeriodicExcitationDetail

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_PERIODIC_EXCITATION_DETAIL

    def __init__(self, instance_to_wrap: 'ElectricMachinePeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
