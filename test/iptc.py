# -*- coding: utf-8 -*-

# ******************************************************************************
#
# Copyright (C) 2009-2011 Olivier Tilloy <olivier@tilloy.net>
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

import unittest

from pyexiv2.iptc import IptcTag, IptcValueError
from pyexiv2.utils import FixedOffset

import datetime
import warnings


class TestIptcTag(unittest.TestCase):

    def test_convert_to_python_short(self):
        # Valid values
        tag = IptcTag('Iptc.Envelope.FileFormat')
        self.assertEqual(tag.type, 'Short')
        self.assertEqual(tag._convert_to_python('23'), 23)
        self.assertEqual(tag._convert_to_python('+5628'), 5628)
        self.assertEqual(tag._convert_to_python('-4'), -4)

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, 'abc')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '5,64')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '47.0001')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '1E3')

    def test_convert_to_string_short(self):
        # Valid values
        tag = IptcTag('Iptc.Envelope.FileFormat')
        self.assertEqual(tag.type, 'Short')
        self.assertEqual(tag._convert_to_string(123), '123')
        self.assertEqual(tag._convert_to_string(-57), '-57')

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(IptcValueError, tag._convert_to_string, 3.14)

    def test_convert_to_python_string(self):
        # Valid values
        tag = IptcTag('Iptc.Application2.Subject')
        self.assertEqual(tag.type, 'String')
        self.assertEqual(tag._convert_to_python('Some text.'), 'Some text.')
        self.assertEqual(tag._convert_to_python('Some text with exotic chàräctérʐ.'),
                         'Some text with exotic chàräctérʐ.')

    def test_convert_to_string_string(self):
        # Valid values
        tag = IptcTag('Iptc.Application2.Subject')
        self.assertEqual(tag.type, 'String')
        self.assertEqual(tag._convert_to_string('Some text'), b'Some text')
        self.assertEqual(tag._convert_to_string('Some text with exotic chàräctérʐ.'),
                         b'Some text with exotic ch\xc3\xa0r\xc3\xa4ct\xc3\xa9r\xca\x90.')

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_string, None)

    def test_convert_to_python_date(self):
        # Valid values
        tag = IptcTag('Iptc.Envelope.DateSent')
        self.assertEqual(tag.type, 'Date')
        self.assertEqual(tag._convert_to_python('1999-10-13'),
                         datetime.date(1999, 10, 13))

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, 'invalid')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '11/10/1983')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '-1000')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '2009-02')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '2009-10-32')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '2009-02-24T22:12:54')

    def test_convert_to_string_date(self):
        # Valid values
        tag = IptcTag('Iptc.Envelope.DateSent')
        self.assertEqual(tag.type, 'Date')
        self.assertEqual(tag._convert_to_string(datetime.date(2009, 2, 4)),
                         '2009-02-04')
        self.assertEqual(tag._convert_to_string(datetime.date(1899, 12, 31)),
                         '1899-12-31')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1999, 10, 13)),
                         '1999-10-13')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2009, 2, 4)),
                         '2009-02-04')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31)),
                         '1899-12-31')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2009, 2, 4, 10, 52, 37)),
                         '2009-02-04')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59)),
                         '1899-12-31')

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_string, 'invalid')
        self.failUnlessRaises(IptcValueError, tag._convert_to_string, None)

    def test_convert_to_python_time(self):
        # Valid values
        tag = IptcTag('Iptc.Envelope.TimeSent')
        self.assertEqual(tag.type, 'Time')
        self.assertEqual(tag._convert_to_python('05:03:54+00:00'),
                         datetime.time(5, 3, 54, tzinfo=FixedOffset()))
        self.assertEqual(tag._convert_to_python('05:03:54+06:00'),
                         datetime.time(5, 3, 54, tzinfo=FixedOffset('+', 6, 0)))
        self.assertEqual(tag._convert_to_python('05:03:54-10:30'),
                         datetime.time(5, 3, 54, tzinfo=FixedOffset('-', 10, 30)))

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, 'invalid')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '23:12:42')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '25:12:42+00:00')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '21:77:42+00:00')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '21:12:98+00:00')
        self.failUnlessRaises(IptcValueError, tag._convert_to_python, '081242+0000')

    def test_convert_to_string_time(self):
        # Valid values
        tag = IptcTag('Iptc.Envelope.TimeSent')
        self.assertEqual(tag.type, 'Time')
        self.assertEqual(tag._convert_to_string(datetime.time(10, 52, 4)),
                         '10:52:04+00:00')
        self.assertEqual(tag._convert_to_string(datetime.time(10, 52, 4, 574)),
                         '10:52:04+00:00')
        self.assertEqual(tag._convert_to_string(datetime.time(10, 52, 4, tzinfo=FixedOffset())),
                         '10:52:04+00:00')
        self.assertEqual(tag._convert_to_string(datetime.time(10, 52, 4, tzinfo=FixedOffset('+', 5, 30))),
                         '10:52:04+05:30')
        self.assertEqual(tag._convert_to_string(datetime.time(10, 52, 4, tzinfo=FixedOffset('-', 4, 0))),
                         '10:52:04-04:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59)),
                         '23:59:59+00:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2007, 2, 7, 10, 52, 4)),
                         '10:52:04+00:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, 999)),
                         '23:59:59+00:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2007, 2, 7, 10, 52, 4, 478)),
                         '10:52:04+00:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset())),
                         '23:59:59+00:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2007, 2, 7, 10, 52, 4, tzinfo=FixedOffset())),
                         '10:52:04+00:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset('+', 5, 30))),
                         '23:59:59+05:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2007, 2, 7, 10, 52, 4, tzinfo=FixedOffset('+', 5, 30))),
                         '10:52:04+05:30')
        self.assertEqual(tag._convert_to_string(datetime.datetime(1899, 12, 31, 23, 59, 59, tzinfo=FixedOffset('-', 4, 0))),
                         '23:59:59-04:00')
        self.assertEqual(tag._convert_to_string(datetime.datetime(2007, 2, 7, 10, 52, 4, tzinfo=FixedOffset('-', 4, 0))),
                         '10:52:04-04:00')

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_string, 'invalid')

    def test_convert_to_python_undefined(self):
        # Valid values
        tag = IptcTag('Iptc.Application2.Preview')
        self.assertEqual(tag.type, 'Undefined')
        self.assertEqual(tag._convert_to_python('Some binary data.'),
                         'Some binary data.')
        self.assertEqual(tag._convert_to_python('�lj1�eEϟ�u����ᒻ;C(�SpI]���QI�}'),
                         '�lj1�eEϟ�u����ᒻ;C(�SpI]���QI�}')

    def test_convert_to_string_undefined(self):
        # Valid values
        tag = IptcTag('Iptc.Application2.Preview')
        self.assertEqual(tag.type, 'Undefined')
        self.assertEqual(tag._convert_to_string('Some binary data.'),
                         'Some binary data.')
        self.assertEqual(tag._convert_to_string('�lj1�eEϟ�u����ᒻ;C(�SpI]���QI�}'),
                         '�lj1�eEϟ�u����ᒻ;C(�SpI]���QI�}')

        # Invalid values
        self.failUnlessRaises(IptcValueError, tag._convert_to_string, None)

    def test_set_single_value_raises(self):
        tag = IptcTag('Iptc.Application2.City', ['Seattle'])
        self.failUnlessRaises(TypeError, setattr, tag, 'value', 'Barcelona')

    def test_set_value(self):
        tag = IptcTag('Iptc.Application2.City', ['Seattle'])
        old_value = tag.value
        tag.value = ['Barcelona']
        self.failIfEqual(tag.value, old_value)

    def test_set_raw_value_invalid(self):
        tag = IptcTag('Iptc.Envelope.DateSent')
        value = ['foo']
        self.failUnlessRaises(ValueError, setattr, tag, 'raw_value', value)

    def test_set_value_non_repeatable(self):
        tag = IptcTag('Iptc.Application2.ReleaseDate')
        value = [datetime.date.today(), datetime.date.today()]
        self.failUnlessRaises(KeyError, setattr, tag, 'value', value)


