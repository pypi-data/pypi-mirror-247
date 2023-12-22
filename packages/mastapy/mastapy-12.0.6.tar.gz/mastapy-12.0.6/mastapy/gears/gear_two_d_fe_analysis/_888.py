﻿"""_888.py

CylindricalGearMeshTIFFAnalysisDutyCycle
"""


from mastapy.gears.analysis import _1212
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_TIFF_ANALYSIS_DUTY_CYCLE = python_net_import('SMT.MastaAPI.Gears.GearTwoDFEAnalysis', 'CylindricalGearMeshTIFFAnalysisDutyCycle')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshTIFFAnalysisDutyCycle',)


class CylindricalGearMeshTIFFAnalysisDutyCycle(_1212.GearMeshDesignAnalysis):
    """CylindricalGearMeshTIFFAnalysisDutyCycle

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_MESH_TIFF_ANALYSIS_DUTY_CYCLE

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshTIFFAnalysisDutyCycle.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()
