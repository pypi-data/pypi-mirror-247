﻿"""_2413.py

GuideImage
"""


from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_GUIDE_IMAGE = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideImage')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideImage',)


class GuideImage(_0.APIBase):
    """GuideImage

    This is a mastapy class.
    """

    TYPE = _GUIDE_IMAGE

    def __init__(self, instance_to_wrap: 'GuideImage.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def distance_from_left_to_origin(self) -> 'float':
        """float: 'DistanceFromLeftToOrigin' is the original name of this property."""

        temp = self.wrapped.DistanceFromLeftToOrigin

        if temp is None:
            return 0.0

        return temp

    @distance_from_left_to_origin.setter
    def distance_from_left_to_origin(self, value: 'float'):
        self.wrapped.DistanceFromLeftToOrigin = float(value) if value is not None else 0.0

    @property
    def distance_from_top_to_centre(self) -> 'float':
        """float: 'DistanceFromTopToCentre' is the original name of this property."""

        temp = self.wrapped.DistanceFromTopToCentre

        if temp is None:
            return 0.0

        return temp

    @distance_from_top_to_centre.setter
    def distance_from_top_to_centre(self, value: 'float'):
        self.wrapped.DistanceFromTopToCentre = float(value) if value is not None else 0.0

    @property
    def image(self) -> 'Image':
        """Image: 'Image' is the original name of this property."""

        temp = self.wrapped.Image

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)
        return value

    @image.setter
    def image(self, value: 'Image'):
        value = conversion.mp_to_pn_smt_bitmap(value)
        self.wrapped.Image = value

    @property
    def image_height(self) -> 'float':
        """float: 'ImageHeight' is the original name of this property.

        Note:
            This property is readonly.
        """

        temp = self.wrapped.ImageHeight

        if temp is None:
            return 0.0

        return temp

    @property
    def image_width(self) -> 'float':
        """float: 'ImageWidth' is the original name of this property."""

        temp = self.wrapped.ImageWidth

        if temp is None:
            return 0.0

        return temp

    @image_width.setter
    def image_width(self, value: 'float'):
        self.wrapped.ImageWidth = float(value) if value is not None else 0.0

    @property
    def transparency(self) -> 'float':
        """float: 'Transparency' is the original name of this property."""

        temp = self.wrapped.Transparency

        if temp is None:
            return 0.0

        return temp

    @transparency.setter
    def transparency(self, value: 'float'):
        self.wrapped.Transparency = float(value) if value is not None else 0.0
