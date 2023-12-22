﻿"""_5683.py

ElectricMachineStatorToothTangentialLoadsExcitationDetail
"""


from mastapy.system_model.analyses_and_results.harmonic_analyses import _5681
from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_STATOR_TOOTH_TANGENTIAL_LOADS_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ElectricMachineStatorToothTangentialLoadsExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineStatorToothTangentialLoadsExcitationDetail',)


class ElectricMachineStatorToothTangentialLoadsExcitationDetail(_5681.ElectricMachineStatorToothLoadsExcitationDetail):
    """ElectricMachineStatorToothTangentialLoadsExcitationDetail

    This is a mastapy class.
    """

    TYPE = _ELECTRIC_MACHINE_STATOR_TOOTH_TANGENTIAL_LOADS_EXCITATION_DETAIL

    def __init__(self, instance_to_wrap: 'ElectricMachineStatorToothTangentialLoadsExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
