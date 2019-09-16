# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2006-2011 Olivier Tilloy <olivier@tilloy.net>
# Copyright (C) 2015-2019 Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>
#
# This file is part of the py3exiv2 distribution.
#
# py3exiv2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.
#
# py3exiv2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with py3exiv2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
#
# Maintainer: Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>
#
# ******************************************************************************

"""
Provide the ImageMetadata class.
"""

import os
import sys
import codecs

from errno import ENOENT
from itertools import chain

if sys.version_info < (3, 3):
    from collections import MutableMapping
else:
    from collections.abc import MutableMapping

import libexiv2python

from pyexiv2.exif import ExifTag, ExifThumbnail
from pyexiv2.iptc import IptcTag
from pyexiv2.xmp import XmpTag
from pyexiv2.preview import Preview


class ImageMetadata(MutableMapping):
    """A container for all the metadata embedded in an image.

    It provides convenient methods for the manipulation of EXIF, IPTC and XMP
    metadata embedded in image files such as JPEG and TIFF files, using Python
    types.
    It also provides access to the previews embedded in an image.
    """

    def __init__(self, filename):
        """Instanciate the ImageMeatadata class.

        Args:
        filename: str(path to an image file)
        """
        self.filename = filename
        self.__image = None
        self._keys = {'exif': None, 'iptc': None, 'xmp': None}
        self._tags = {'exif': {}, 'iptc': {}, 'xmp': {}}
        self._exif_thumbnail = None

    def _instantiate_image(self, filename):
        """Instanciate the exiv2 image.

        Args:
        filename -- str(path to an image file)
        """
        # This method is meant to be overridden in unit tests to easily replace
        # the internal image reference by a mock.
        if not os.path.exists(filename) or not os.path.isfile(filename):
            raise IOError(ENOENT, os.strerror(ENOENT), filename)

        # Remember the reference timestamps before doing any access to the file
        stat = os.stat(filename)
        self._atime = stat.st_atime
        self._mtime = stat.st_mtime
        return libexiv2python._Image(filename)

    @classmethod
    def from_buffer(cls, buffer_):
        """Instantiate an image container from an image memoryview.

        Args:
        buffer_ -- a memoryview containing image data as bytes
        """
        obj = cls(None)
        obj.__image = libexiv2python._Image(buffer_, len(buffer_))
        return obj

    @property
    def _image(self):
        if self.__image is None:
            raise IOError('Image metadata has not been read yet')

        return self.__image

    def read(self):
        """Read the metadata embedded in the associated image.

        It is necessary to call this method once before attempting to access
        the metadata (an exception will be raised if trying to access metadata
        before calling this method).
        """
        if self.__image is None:
            self.__image = self._instantiate_image(self.filename)

        self.__image._readMetadata()

    def write(self, preserve_timestamps=False):
        """Write the metadata back to the image.

        Args:
        preserve_timestamps -- whether to preserve the file's original
                               timestamps (access time and modification time)
                               Type: boolean
        """
        self._image._writeMetadata()
        if self.filename is None:
            return

        if preserve_timestamps:
            # Revert to the original timestamps
            os.utime(self.filename, (self._atime, self._mtime))

        else:
            # Reset the reference timestamps
            stat = os.stat(self.filename)
            self._atime = stat.st_atime
            self._mtime = stat.st_mtime

    @property
    def dimensions(self):
        """A tuple containing the width and height of the image, expressed in
        pixels.

        """
        return (self._image._getPixelWidth(), self._image._getPixelHeight())

    @property
    def mime_type(self):
        """The mime type of the image, as a string.

        """
        return self._image._getMimeType()

    @property
    def exif_keys(self):
        """Return the list of the keys of the available EXIF tags.

        """
        if self._keys['exif'] is None:
            self._keys['exif'] = self._image._exifKeys()

        return self._keys['exif']

    @property
    def iptc_keys(self):
        """Return the list of the keys of the available IPTC tags.

        """
        if self._keys['iptc'] is None:
            self._keys['iptc'] = self._image._iptcKeys()

        return self._keys['iptc']

    @property
    def xmp_keys(self):
        """Return the list of the keys of the available XMP tags.

        """
        if self._keys['xmp'] is None:
            self._keys['xmp'] = self._image._xmpKeys()

        return self._keys['xmp']

    def _get_exif_tag(self, key):
        """Return the EXIF tag for the given key.

        Throw a KeyError if the tag doesn't exist.

        Args:
        key -- the exif key
        """
        try:
            return self._tags['exif'][key]
        except KeyError:
            _tag = self._image._getExifTag(key)
            tag = ExifTag._from_existing_tag(_tag)
            self._tags['exif'][key] = tag
            return tag

    def _get_iptc_tag(self, key):
        """Return the IPTC tag for the given key.

        Throw a KeyError if the tag doesn't exist.

        Args:
        key -- the iptc key
        """
        try:
            return self._tags['iptc'][key]
        except KeyError:
            _tag = self._image._getIptcTag(key)
            tag = IptcTag._from_existing_tag(_tag)
            self._tags['iptc'][key] = tag
            return tag

    def _get_xmp_tag(self, key):
        """Return the XMP tag for the given key.

        Throw a KeyError if the tag doesn't exist.

        Args:
        key -- the xmp key
        """
        try:
            return self._tags['xmp'][key]
        except KeyError:
            _tag = self._image._getXmpTag(key)
            tag = XmpTag._from_existing_tag(_tag)
            self._tags['xmp'][key] = tag
            return tag

    def __getitem__(self, key):
        """Return a metadata tag for a given key.

        Raise KeyError if the tag doesn't exist

        Args:
        key -- metadata key in the dotted form
               ``familyName.groupName.tagName`` where ``familyName`` may
               be one of ``exif``, ``iptc`` or ``xmp``.
        """
        family = key.split('.')[0].lower()
        if family in ('exif', 'iptc', 'xmp'):
            return getattr(self, '_get_%s_tag' % family)(key)

        else:
            raise KeyError(key)

    def _set_exif_tag(self, key, tag_or_value):
        """Set an EXIF tag. If the tag already exists, its value is overwritten.

        Args:
        key -- the EXIF key
        tag_or_value -- an ExifTag instance or the value of the data
        """
        if isinstance(tag_or_value, ExifTag):
            tag = tag_or_value

        else:
            # As a handy shortcut, accept direct value assignment.
            tag = ExifTag(key, tag_or_value)

        tag._set_owner(self)
        self._tags['exif'][tag.key] = tag
        if tag.key not in self.exif_keys:
            self._keys['exif'].append(tag.key)

    def _set_iptc_tag(self, key, tag_or_values):
        """Set an IPTC tag. If the tag already exists, its value is overwritten.

        Args:
        key -- the IPTC key
        tag_or_value -- an IptcTag instance or the value of the data
        """
        if isinstance(tag_or_values, IptcTag):
            tag = tag_or_values

        else:
            # As a handy shortcut, accept direct value assignment.
            tag = IptcTag(key, tag_or_values)

        tag._set_owner(self)
        self._tags['iptc'][tag.key] = tag
        if tag.key not in self.iptc_keys:
            self._keys['iptc'].append(tag.key)

    def _set_xmp_tag(self, key, tag_or_value):
        """Set an XMP tag. If the tag already exists, its value is overwritten.

        Args:
        key -- the XMP key
        tag_or_value -- an XmpTag instance or the value of the data
        """
        if isinstance(tag_or_value, XmpTag):
            tag = tag_or_value

        else:
            # As a handy shortcut, accept direct value assignment.
            tag = XmpTag(key, tag_or_value)

        tag._set_owner(self)
        self._tags['xmp'][tag.key] = tag
        if tag.key not in self.xmp_keys:
            self._keys['xmp'].append(tag.key)

    def __setitem__(self, key, tag_or_value):
        """Set a metadata tag for a given key.

        If the tag was previously set, it is overwritten.
        As a handy shortcut, a value may be passed instead of a fully formed
        tag. The corresponding tag object will be instantiated.

        Raise KeyError if the key is invalid

        Args:
        key -- metadata key in the dotted form
               ``familyName.groupName.tagName`` where ``familyName`` may
               be one of ``exif``, ``iptc`` or ``xmp``.
        tag_or_value -- an instance of the corresponding family of metadata
                        tag or a value
                        Type: pyexiv2.exif.ExifTag instance or
                              pyexiv2.iptc.IptcTag instance or
                              pyexiv2.xmp.XmpTag instance or 
                              any valid value type
        """
        family = key.split('.')[0].lower()
        if family in ('exif', 'iptc', 'xmp'):
            return getattr(self, '_set_%s_tag' % family)(key, tag_or_value)

        else:
            raise KeyError(key)

    def _delete_exif_tag(self, key):
        """Delete an EXIF tag.

        Throw a KeyError if the tag doesn't exist.

        Args:
        key -- the EXIF key
        """
        if key not in self.exif_keys:
            raise KeyError('Cannot delete an inexistent tag')

        self._image._deleteExifTag(key)
        try:
            del self._tags['exif'][key]
        except KeyError:
            # The tag was not cached.
            pass

        if self._keys['exif'] is not None:
            self._keys['exif'].remove(key)

    def _delete_iptc_tag(self, key):
        """Delete an IPTC tag.

        Throw a KeyError if the tag doesn't exist.

        Args:
        key -- the IPTC key
        """
        if key not in self.iptc_keys:
            raise KeyError('Cannot delete an inexistent tag')

        self._image._deleteIptcTag(key)
        try:
            del self._tags['iptc'][key]
        except KeyError:
            # The tag was not cached.
            pass

        if self._keys['iptc'] is not None:
            self._keys['iptc'].remove(key)

    def _delete_xmp_tag(self, key):
        """Delete an XMP tag.

        Throw a KeyError if the tag doesn't exist.

        Args:
        key -- the XMP key
        """
        if key not in self.xmp_keys:
            raise KeyError('Cannot delete an inexistent tag')

        self._image._deleteXmpTag(key)
        try:
            del self._tags['xmp'][key]
        except KeyError:
            # The tag was not cached.
            pass

        if self._keys['xmp'] is not None:
            self._keys['xmp'].remove(key)

    def __delitem__(self, key):
        """Delete a metadata tag for a given key.

        Raise KeyError if the tag with the given key doesn't exist

        Args:
        key -- the metadata key in the dotted form
               ``familyName.groupName.tagName`` where ``familyName`` may
               be one of ``exif``, ``iptc`` or ``xmp``.
        """
        family = key.split('.')[0].lower()
        if family in ('exif', 'iptc', 'xmp'):
            return getattr(self, '_delete_%s_tag' % family)(key)

        else:
            raise KeyError(key)

    def __iter__(self):
        return chain(self.exif_keys, self.iptc_keys, self.xmp_keys)

    def __len__(self):
        return len([x for x in self])

    def _get_comment(self):
        return self._image._getComment()

    def _set_comment(self, comment):
        if comment is not None:
            self._image._setComment(comment)

        else:
            self._del_comment()

    def _del_comment(self):
        self._image._clearComment()

    comment = property(fget=_get_comment, fset=_set_comment, fdel=_del_comment,
                       doc='The image comment.')

    @property
    def previews(self):
        """List of the previews available in the image, sorted by increasing
        size.

        """
        return [Preview(preview) for preview in self._image._previews()]

    def copy(self, other, exif=True, iptc=True, xmp=True, comment=True):
        """Copy the metadata to another image.

        The metadata in the destination is overridden. In particular, if the
        destination contains e.g. EXIF data and the source doesn't, it will be
        erased in the destination, unless explicitly omitted.

        Args:
        other -- the destination metadata to copy to (it must have been
                 read beforehand)
                 Type: pyexiv2.metadata.ImageMetadata instance
        exif -- whether to copy the EXIF metadata, default True
        iptc -- whether to copy the IPTC metadata, default True
        xmp -- whether to copy the XMP metadata, default True
        comment -- whether to copy the image comment, default True 
        """
        self._image._copyMetadata(other._image, exif, iptc, xmp)
        # Empty the cache where needed
        if exif:
            other._keys['exif'] = None
            other._tags['exif'] = {}

        if iptc:
            other._keys['iptc'] = None
            other._tags['iptc'] = {}

        if xmp:
            other._keys['xmp'] = None
            other._tags['xmp'] = {}

        if comment:
            other.comment = self.comment

    @property
    def buffer(self):
        """
        The image buffer as a string.
        If metadata has been modified, the data won't be up-to-date until
        :meth:`.write` has been called.
        """
        return self._image._getDataBuffer()

    @property
    def exif_thumbnail(self):
        """A thumbnail image optionally embedded in the EXIF data.

        """
        if self._exif_thumbnail is None:
            self._exif_thumbnail = ExifThumbnail(self)

        return self._exif_thumbnail

    def _get_iptc_charset(self):
        value = self._image._getIptcCharset()
        if value != '':
            return value.lower()

        else:
            return None

    def _set_iptc_charset(self, charset):
        if charset is None:
            self._del_iptc_charset()
            return

        try:
            name = codecs.lookup(charset).name
        except LookupError as error:
            raise ValueError(error)

        else:
            charsets = {'utf-8': '\x1b%G'}
            try:
                self['Iptc.Envelope.CharacterSet'] = (charsets[name],)
            except KeyError:
                raise ValueError('Unhandled charset: %s' % name)

    def _del_iptc_charset(self):
        try:
            del self['Iptc.Envelope.CharacterSet']
        except KeyError:
            pass

    iptc_charset = property(fget=_get_iptc_charset, 
                            fset=_set_iptc_charset,
                            fdel=_del_iptc_charset,
                            doc='An optional character set the IPTC data'\
                                ' is encoded in.')

    # Some convenient functions -------------------------------------------
    def get_iso(self):
        """Returns the ISO value as integer.

        """
        try:
            return self["Exif.Photo.ISOSpeedRatings"].value
        except KeyError:
            return

    def get_shutter_speed(self, float_=False):
        """Returns the exposure time as rational or float.

        Args:
        float_ -- if False, default, the value is returned as rational 
                  otherwise as float
        """
        try:
            speed = self['Exif.Photo.ExposureTime'].value 
        except KeyError:
            return

        if float_:
            if speed.denominator:
                return speed.numerator / speed.denominator
            return float(numerator)

        return speed

    def get_focal_length(self):
        """Returns the focal length as float.

        """
        try:
            focal = self['Exif.Photo.FocalLength'].value
            if focal.denominator:
                return round(focal.numerator / focal.denominator, 2)

            else:
                return float(focal.numerator)

        except KeyError:
            return

    def get_aperture(self):
        """Returns the fNumber as float.

        """
        try:
            fnumber = self["Exif.Photo.FNumber"].value
            if fnumber.denominator:
                return round(fnumber.numerator / fnumber.denominator, 2)

            else:
                return float(fnumber.numerator)
        except KeyError:
            return

    def get_orientation(self):
        """Returns the orientation of the image as integer.

        If the tag is not set, the value 1 is returned.
        """
        try:
            return self["Exif.Image.Orientation"].value
        except KeyError:
            return 1

    def get_exposure_data(self, float_=False):
        """Returns the exposure parameters of the image.

        The values are returned as a dict which contains:
            "iso": the ISO value
            "speed": the exposure time
            "focal": the focal length
            "aperture": the fNumber
            "orientation": the orientation of the image

        When a tag is not set, the value will be None

        Args:
        float_ -- if False, default, the value of the exposure time is returned 
                  as rational otherwise as float
        """
        data = {"iso": self.get_iso(),
                "speed": self.get_shutter_speed(float_),
                "focal": self.get_focal_length(),
                "aperture": self.get_aperture(),
                "orientation": self.get_orientation()}

        return data

    def get_rights_data(self):
        """Returns the author and copyright info.

        The values are returned as a dict which contains:
            "creator": the value of Xmp.dc.creator
            "artist": the value of Exif.Image.Artist
            "rights": the value of Xmp.dc.rights
            "copyright": the value of Exif.Image.Copyright
            "marked": the value of Xmp.xmpRights.Marked
            "usage": the value of Xmp.xmpRights.UsageTerms

        When a tag is not set, the value will be None
        """
        tags = [('creator', 'Xmp.dc.creator'), 
                ('artist', 'Exif.Image.Artist'),
                ('rights', 'Xmp.dc.rights'), 
                ('copyright', 'Exif.Image.Copyright'),
                ('marked', 'Xmp.xmpRights.Marked'), 
                ('usage', 'Xmp.xmpRights.UsageTerms')]
        rights = {}
        for tag in tags:
            try:
                rights[tag[0]] = self[tag[1]].value
            except KeyError:
                rights[tag[0]] = None

        return rights


