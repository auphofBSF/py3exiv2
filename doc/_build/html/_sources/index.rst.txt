.. py3exiv2 documentation master file, created by
   sphinx-quickstart on Mon Jan 19 15:06:54 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to py3exiv2's documentation!
====================================

py3exiv2 is a `Python 3 <https://docs.python.org/3/>`_ binding to 
`exiv2 <http://exiv2.org/>`_, the C++ library
for manipulation of :abbr:`EXIF (EXchangeable Image File)`,
:abbr:`IPTC (International Press Telecommunications Council)` and
:abbr:`XMP (eXtensible Metadata Platform)` image metadata.
It is a python 3 module that allows your scripts to read and write metadata (EXIF, IPTC, XMP, thumbnails) embedded in image files (JPEG, TIFF, ...).

It is designed as a high-level interface to the functionalities offered by
libexiv2. Using python's built-in data types and standard modules, it provides
easy manipulation of image metadata.

py3exiv2 is distributed under the
`GPL version 3 <http://www.gnu.org/licenses/gpl.html>`_
license.

The main content of the code was initially written by Olivier Tilloy for 
Python 2 under the name `pyexiv2 <http://tilloy.net/dev/pyexiv2/index.html>`_.

**Differences between py3exiv2 (Python 3) and pyexiv2 (Python 2)**

The module's name and the syntax are unchanged, your code written previously for Python 2 may run with py3exiv2, however there's three thinks that you should be care.

   * The deprecated ``IptcTag.raw_values`` was removed in py3exiv2, use ``IptcTag.raw_value`` instead.
   * The ``pyexiv2.preview.Preview.data`` is not implemented, use ``pyexiv2.exif.ExifThumbnail.data`` instead.
   * All the string returned by any ``Tag.value`` are unicode, but you don't need to convert yours strings in bytes to set a value for a tag which only accept ASCII characters, this is the job of py3exiv2.


Contents:

.. toctree::
   :maxdepth: 2

   api.rst
   tutorial.rst
   developers.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

