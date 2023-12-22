﻿"""_2452.py

ConceptBearingFromCAD
"""


from mastapy._internal import constructor
from mastapy.system_model.part_model.import_from_cad import _2453
from mastapy._internal.python_net import python_net_import

_CONCEPT_BEARING_FROM_CAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ImportFromCAD', 'ConceptBearingFromCAD')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptBearingFromCAD',)


class ConceptBearingFromCAD(_2453.ConnectorFromCAD):
    """ConceptBearingFromCAD

    This is a mastapy class.
    """

    TYPE = _CONCEPT_BEARING_FROM_CAD

    def __init__(self, instance_to_wrap: 'ConceptBearingFromCAD.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def width(self) -> 'float':
        """float: 'Width' is the original name of this property."""

        temp = self.wrapped.Width

        if temp is None:
            return 0.0

        return temp

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value is not None else 0.0
