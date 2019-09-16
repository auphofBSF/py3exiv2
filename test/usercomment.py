# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2010 Olivier Tilloy <olivier@tilloy.net>
# Copyright (C) 2015-2016 Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>
#
# This file is part of the pyexiv2 distribution.
#
# pyexiv2 is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# pyexiv2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyexiv2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.
#
# Maintainer: Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>
#
# ******************************************************************************

from pyexiv2.metadata import ImageMetadata

import unittest
import testutils
import os
import tempfile
from testutils import EMPTY_JPG_DATA


class TestUserCommentReadWrite(unittest.TestCase):

    checksums = {
        'usercomment-ascii.jpg': 'ad29ac65fb6f63c8361aaed6cb02f8c7',
        'usercomment-unicode-ii.jpg': '13b7cc09129a8677f2cf18634f5abd3c',
        'usercomment-unicode-mm.jpg': '7addfed7823c556ba489cd4ab2037200',
        }

    def _read_image(self, filename):
        filepath = testutils.get_absolute_file_path(os.path.join('data', filename))
        self.assert_(testutils.CheckFileSum(filepath, self.checksums[filename]))
        m = ImageMetadata(filepath)
        m.read()
        return m

    def test_read_ascii(self):
        m = self._read_image('usercomment-ascii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag.raw_value, 'charset="Ascii" deja vu')
        self.assertEqual(tag.value, 'deja vu')

    def test_write_ascii(self):
        m = self._read_image('usercomment-ascii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        tag.value = 'foo bar'
        self.assertEqual(tag.raw_value, b'foo bar')
        self.assertEqual(tag.value, 'foo bar')

    def test_write_unicode_over_ascii(self):
        m = self._read_image('usercomment-ascii.jpg')
        tag = m['Exif.Photo.UserComment']
        self.assertEqual(tag.type, 'Comment')
        tag.value = 'déjà vu'
        self.assertEqual(tag.raw_value, b'd\xc3\xa9j\xc3\xa0 vu')
        self.assertEqual(tag.value, 'déjà vu')

class TestUserCommentAdd(unittest.TestCase):

    def setUp(self):
        # Create an empty image file
        fd, self.pathname = tempfile.mkstemp(suffix='.jpg')
        os.write(fd, EMPTY_JPG_DATA)
        os.close(fd)

    def tearDown(self):
        os.remove(self.pathname)

    def _test_add_comment(self, value):
        metadata = ImageMetadata(self.pathname)
        metadata.read()
        key = 'Exif.Photo.UserComment'
        metadata[key] = value
        metadata.write()

        metadata = ImageMetadata(self.pathname)
        metadata.read()
        self.assert_(key in metadata.exif_keys)
        tag = metadata[key]
        self.assertEqual(tag.type, 'Comment')
        self.assertEqual(tag.value, value)

    def test_add_comment_ascii(self):
        self._test_add_comment('deja vu')

    def test_add_comment_unicode(self):
        self._test_add_comment('déjà vu')

