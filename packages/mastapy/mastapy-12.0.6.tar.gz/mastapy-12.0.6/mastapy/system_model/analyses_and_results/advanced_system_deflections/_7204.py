﻿"""_7204.py

AdvancedSystemDeflection
"""


from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7205
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.analysis_cases import _7480
from mastapy._internal.python_net import python_net_import

_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'AdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflection',)


class AdvancedSystemDeflection(_7480.StaticLoadAnalysisCase):
    """AdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _ADVANCED_SYSTEM_DEFLECTION

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def advanced_system_deflection_options(self) -> '_7205.AdvancedSystemDeflectionOptions':
        """AdvancedSystemDeflectionOptions: 'AdvancedSystemDeflectionOptions' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AdvancedSystemDeflectionOptions

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None
