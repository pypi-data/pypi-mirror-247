﻿"""_5809.py

ResultsForResponseOfANodeOnAHarmonic
"""


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import _5810, _5791
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults', 'ResultsForResponseOfANodeOnAHarmonic')


__docformat__ = 'restructuredtext en'
__all__ = ('ResultsForResponseOfANodeOnAHarmonic',)


class ResultsForResponseOfANodeOnAHarmonic(_0.APIBase):
    """ResultsForResponseOfANodeOnAHarmonic

    This is a mastapy class.
    """

    TYPE = _RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC

    def __init__(self, instance_to_wrap: 'ResultsForResponseOfANodeOnAHarmonic.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def angular_magnitude(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'AngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.AngularMagnitude

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def linear_magnitude(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'LinearMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.LinearMagnitude

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def radial_angular_magnitude(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'RadialAngularMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialAngularMagnitude

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def radial_magnitude(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'RadialMagnitude' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RadialMagnitude

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def result_at_reference_speed(self) -> '_5791.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic':
        """DatapointForResponseOfANodeAtAFrequencyOnAHarmonic: 'ResultAtReferenceSpeed' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ResultAtReferenceSpeed

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def theta_x(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'ThetaX' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThetaX

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def theta_y(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'ThetaY' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThetaY

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def theta_z(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'ThetaZ' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ThetaZ

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def x(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'X' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.X

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def y(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'Y' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Y

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def z(self) -> '_5810.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic':
        """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic: 'Z' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.Z

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def data_points(self) -> 'List[_5791.DatapointForResponseOfANodeAtAFrequencyOnAHarmonic]':
        """List[DatapointForResponseOfANodeAtAFrequencyOnAHarmonic]: 'DataPoints' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.DataPoints

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)
        return value
