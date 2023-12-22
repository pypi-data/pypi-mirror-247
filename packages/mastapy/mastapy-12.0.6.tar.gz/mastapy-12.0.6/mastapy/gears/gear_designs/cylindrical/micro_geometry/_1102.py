﻿"""_1102.py

CylindricalGearTriangularEndModification
"""


from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1103
from mastapy._internal import constructor
from mastapy.gears.micro_geometry import _572
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry', 'CylindricalGearTriangularEndModification')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTriangularEndModification',)


class CylindricalGearTriangularEndModification(_572.Modification):
    """CylindricalGearTriangularEndModification

    This is a mastapy class.
    """

    TYPE = _CYLINDRICAL_GEAR_TRIANGULAR_END_MODIFICATION

    def __init__(self, instance_to_wrap: 'CylindricalGearTriangularEndModification.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def root_left(self) -> '_1103.CylindricalGearTriangularEndModificationAtOrientation':
        """CylindricalGearTriangularEndModificationAtOrientation: 'RootLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootLeft

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def root_right(self) -> '_1103.CylindricalGearTriangularEndModificationAtOrientation':
        """CylindricalGearTriangularEndModificationAtOrientation: 'RootRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.RootRight

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tip_left(self) -> '_1103.CylindricalGearTriangularEndModificationAtOrientation':
        """CylindricalGearTriangularEndModificationAtOrientation: 'TipLeft' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipLeft

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    @property
    def tip_right(self) -> '_1103.CylindricalGearTriangularEndModificationAtOrientation':
        """CylindricalGearTriangularEndModificationAtOrientation: 'TipRight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.TipRight

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp) if temp is not None else None

    def relief_of(self, face_width: 'float', roll_distance: 'float') -> 'float':
        """ 'ReliefOf' is the original name of this method.

        Args:
            face_width (float)
            roll_distance (float)

        Returns:
            float
        """

        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = self.wrapped.ReliefOf(face_width if face_width else 0.0, roll_distance if roll_distance else 0.0)
        return method_result
