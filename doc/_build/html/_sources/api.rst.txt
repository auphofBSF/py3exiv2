API documentation
=================

pyexiv2
#######

The top-level module :class:`pyexiv2`.

**Attributes**

..

* :ref:`version_info <versioninfo>`
* :ref:`__version__ <version__>`
* :ref:`exiv2_version_info <exiv2versioninfo>`
* :ref:`__exiv2_version__ <exiv2_version__>`

**Description**

Top-level module. All other modules are imported from :class:`pyexiv2`.

**Documentation**

**Attributes**

.. _versioninfo:
.. attribute:: version_info

   A tuple containing the three components of the version number: major, minor, micro.


.. _version__:
.. attribute:: __version__

   The version of the module as a string (major.minor.micro).


.. _exiv2versioninfo:
.. attribute:: exiv2_version_info

   A tuple containing the three components of the version number of libexiv2: major, minor, micro.


.. _exiv2_version__:
.. attribute:: __exiv2_version__

   The version of libexiv2 as a string (major.minor.micro).


pyexiv2.metadata
################

.. class:: pyexiv2.metadata.ImageMetadata

**Instance Attributes**

..

* :ref:`buffer <buffer>`
* :ref:`comment <comment>`
* :ref:`dimensions <dimensions>`
* :ref:`exif_keys <exifkeys>`
* :ref:`iptc_charset <iptccharset>`
* :ref:`iptc_keys <iptckeys>`
* :ref:`mime_type <mimetype>`
* :ref:`previews <previews>`
* :ref:`xmp_keys <xmpkeys>`


**Instance Methods**

..

* :func:`copy(other, exif=True, iptc=True, xmp=True, comment=True) <copy>`
* :func:`__delitem__(key) <__delitem__>`
* :func:`get_aperture(self) <get_aperture>`
* :func:`get_exposure_data(self, float_=False) <get_exposure_data>`
* :func:`get_focal_length(self) <get_focal_length>`
* :func:`get_iso(self) <get_iso>`
* :func:`__getitem__(key) <__getitem__>`
* :func:`get_orientation(self) <get_orientation>`
* :func:`get_rights_data(self) <get_rights_data>`
* :func:`get_shutter_speed(self, float_=False) <get_shutter_speed>`
* :func:`read() <read>`
* :func:`__setitem__(key) <__setitem__>`
* :func:`write(preserve_timestamps=False) <write>`

**Description**

The :class:`pyexiv2.metadata.ImageMetadata` is a container for all the metadata embedded in an image.

It provides convenient methods for the manipulation of EXIF, IPTC and XMP metadata embedded in image files such as JPEG and TIFF files, using Python types. It also provides access to the previews embedded in an image.

**Documentation**

**Instanciation**

.. class:: pyexiv2.metadata.ImageMetadata(filename)

   Inherits: `MutableMapping <https://docs.python.org/3/library/collections.abc.html?highlight=mutablemapping#collections.abc.MutableMapping>`_

   Argument:

      * *filename* str(path of an image file)

   See :func:`read`

**Attributes**

.. _buffer:
.. attribute:: buffer

   Return the image data as bytes.  This is useful to reduce disk access, the data can be send to an image library.

   Example with Pillow::

   >>> from PIL import Image
   >>> import io
   >>> import pyexiv2
   >>> meta = pyexiv2.ImageMetadata("lena.jpg")
   >>> meta.read()
   >>> byteio = io.BytesIO(meta.buffer)
   >>> img = Image.open(byteio)
   >>> img.show()

.. _comment:
.. attribute:: comment

   The image comment.

.. _dimensions:
.. attribute:: dimensions

   A tuple containing the width and height of the image, expressed in pixels.

.. _exifkeys:
.. attribute:: exif_keys

   List of the keys of the available EXIF tags.

.. _iptccharset:
.. attribute:: iptc_charset

   An optional character set the IPTC data is encoded in.

.. _iptckeys:
.. attribute:: iptc_keys

   List of the keys of the available IPTC tags.

.. _mimetype:
.. attribute:: mime_type

   The mime type of the image, as a string.

.. _previews:
.. attribute:: previews

   List of the previews available in the image, sorted by increasing size.

.. _xmpkeys:
.. attribute:: xmp_keys

   List of the keys of the available XMP tags.


**Methods**

.. function:: copy(other, exif=True, iptc=True, xmp=True, comment=True)

   Copy the metadata to another image. The metadata in the destination is overridden. 
   In particular, if the destination contains e.g. EXIF data and the source doesn’t, 
   it will be erased in the destination, unless explicitly omitted.

   Arguments:	

      * *other* An instance of :class:pyexiv2.metadata.ImageMetadata, the destination metadata to copy to (it must have been read() beforehand)
      * *exif* (boolean) – Whether to copy the EXIF metadata
      * *iptc* (boolean) – Whether to copy the IPTC metadata
      * *xmp* (boolean) – Whether to copy the XMP metadata
      * *comment* (boolean) – Whether to copy the image comment


.. function:: __delitem__(key)

   Delete a metadata tag for a given key.

   Argument:

      * *key* Metadata key in the dotted form *familyName.groupName.tagName* where *familyName* may be one of *exif*, *iptc* or *xmp*.

   Raises KeyError if the tag with the given key doesn’t exist

.. function:: get_aperture(self)

   Returns the fNumber as float.

.. function:: get_exposure_data(self, float_=False)

   Returns the exposure parameters of the image.

   The values are returned as a dict which contains:

      * *"iso"*: the ISO value
      * *"speed"*: the exposure time
      * *"focal"*: the focal length
      * *"aperture"*: the fNumber
      * *"orientation"*: the orientation of the image

   When a tag is not set, the value will be None.

   Argument:

      * *float_* If False, default, the value of the exposure time is returned as rational otherwise a float is returned.

.. function:: get_focal_length(self)

   Returns the focal length as float.

.. function:: get_iso(self)

   Returns the ISO value as integer.

.. function:: __getitem__(key)

   Get a metadata tag for a given key.

   Argument:

      * *key* Metadata key in the dotted form familyName.groupName.tagName where familyName may be one of exif, iptc or xmp.

   Raises KeyError if the tag doesn’t exist

.. function:: get_orientation(self)

   Returns the orientation of the image as integer.

   If the tag is not set, the value 1 is returned.

.. function:: get_rights_data(self)

   Returns the author and copyright info.

   The values are returned as a dict which contains:

      * *"creator"*: the value of Xmp.dc.creator
      * *"artist"*: the value of Exif.Image.Artist
      * *"rights"*: the value of Xmp.dc.rights
      * *"copyright"*: the value of Exif.Image.Copyright
      * *"marked"*: the value of Xmp.xmpRights.Marked
      * *"usage"*: the value of Xmp.xmpRights.UsageTerms

   When a tag is not set, the value will be None.

.. function:: get_shutter_speed(self, float_=False)

   Returns the exposure time as rational or float or None if the tag is not set.

   Argument:

      * *float_* If False, default, the value is returned as rational otherwise a float is returned

.. function:: read()

   Read the metadata embedded in the associated image. It is necessary to call this method once before attempting to access the metadata (an exception will be raised if trying to access metadata before calling this method).

.. function:: __setitem__(key, tag_or_value)

   Set a metadata tag for a given key. If the tag was previously set, it is overwritten. As a handy shortcut, a value may be passed instead of a fully formed tag. The corresponding tag object will be instantiated.

   Arguments:	

      * *key* Metadata key in the dotted form familyName.groupName.tagName where familyName may be one of exif, iptc or xmp.
      * *tag_or_value* (pyexiv2.exif.ExifTag or pyexiv2.iptc.IptcTag or pyexiv2.xmp.XmpTag or any valid value type) – An instance of the corresponding family of metadata tag, or a value

   Raises KeyError if the tag doesn’t exist


.. function:: write(preserve_timestamps=False)

   Write the metadata back to the image.

   Argument:

      * *preserve_timestamps* (boolean) – Whether to preserve the file’s original timestamps (access time and modification time)


pyexiv2.exif
############

This module provides the classes :class:`ExifTag`, :class:`ExifValueError` and :class:`ExifThumbnail`.

.. class:: pyexiv2.exif.ExifTag

**Instance Attributes**

..

* :ref:`description <description>`
* :ref:`human_value <humanvalue>`
* :ref:`key <key>`
* :ref:`label <label>`
* :ref:`name <name>`
* :ref:`raw_value <rawvalue>`
* :ref:`section_description <sectiondescription>`
* :ref:`section_name <sectionname>`
* :ref:`type <type>`
* :ref:`value <value>`

**Description**

The :class:`ExifTag` define an EXIF tag.

**Documentation**

**Instanciation**

.. class:: pyexiv2.exif.ExifTag(key, value=None, _tag=None)

   An EXIF tag.

   Arguments:

      * *key* The key of the tag in the dotted form *familyName.groupName.tagName* where *familyName* = *exif*.
      * *value* The value of the tag.

   Here is a correspondance table between the EXIF types and the possible python types the value of a tag may take:

      * Ascii: datetime.datetime(), datetime.date(), str()
      * Byte, SByte: str()
      * Comment: str()
      * Long, SLong: [list of] int
      * Short, SShort: [list of] int
      * Rational, SRational: [list of] fractions.Fraction
      * Undefined: str()

**Attributes**

.. _description:
.. attribute:: description

   The description of the tag.

.. _humanvalue:
.. attribute:: human_value

   A (read-only) human-readable representation of the value of the tag.

.. _key:
.. attribute:: key

   The key of the tag in the dotted form familyName.groupName.tagName where familyName = exif.

.. _label:
.. attribute:: label

   The title (label) of the tag.

.. _name:
.. attribute:: name

   The name of the tag (this is also the third part of the key).

.. _rawvalue:
.. attribute:: raw_value

   The raw value of the tag as a string.

.. _sectiondescription:
.. attribute:: section_description

   The description of the tag’s section.

.. _sectionname:
.. attribute:: section_name

   The name of the tag’s section.

.. _type:
.. attribute:: type

   The EXIF type of the tag (one of Ascii, Byte, SByte, Comment, Short, SShort, Long, SLong, Rational, SRational, Undefined).

.. _value:
.. attribute:: value

   The value of the tag as a python object.


.. class:: pyexiv2.exif.ExifValueError(value, type)

   Exception raised when failing to parse the value of an EXIF tag.


   Arguments:

      * *value* The value that fails to be parsed
      * *type*	The EXIF type of the tag


.. class:: pyexiv2.exif.ExifThumbnail

**Instance Attributes**

..

* :ref:`extension <extension>`
* :ref:`mime_type <mimetyp>`
* :ref:`data <data>`

**Instance Method**

..

* :func:`erase() <erase>`
* :func:`set_from_file(path) <set_from_file>`
* :func:`write_to_file(path) <write_to_file>`

**Description**

A thumbnail image optionally embedded in the IFD1 segment of the EXIF data.

The image is either a TIFF or a JPEG image.

**Documentation**

**Instanciation**

class pyexiv2.exif.ExifThumbnail(_metadata)

   Argument:

      * *_metadata* The :class:`ImageMetadata` instance

**Attributes**

.. _extension:
.. attribute:: extension

   The file extension of the preview image with a leading dot (e.g. .jpg).

.. _mimetyp:
.. attribute:: mime_type

   The mime type of the preview image (e.g. image/jpeg).

.. _data:
.. data:: data

   The preview data as a Python list. The data can be send to an image library.

   Example with Pillow::

   >>> from PIL import Image
   >>> import io
   >>> from pyexiv2 import ImageMetadata, exif
   >>> meta = ImageMetadata("lena.jpg")
   >>> meta.read()
   >>> thumb = exif.ExifThumbnail(meta)
   >>> byteio = io.BytesIO(bytes(thumb.data))
   >>> img = Image.open(byteio)
   >>> img.show()


**Methods**

.. function:: erase()

   Delete the thumbnail from the EXIF data. Removes all Exif.Thumbnail.*, i.e. Exif IFD1 tags.

.. function:: set_from_file(path)

   Set the EXIF thumbnail to the JPEG image path. This sets only the Compression, JPEGInterchangeFormat and JPEGInterchangeFormatLength tags, which is not all the thumbnail EXIF information mandatory according to the EXIF standard (but it is enough to work with the thumbnail).

   Argument:
      * *path* str(Path to a JPEG file).

.. function:: write_to_file(path)

   Write the thumbnail image to a file on disk. The file extension will be automatically appended to the path.

   Argument:

      * *path* str(Path to write the thumbnail to) - without an extension.


pyexiv2.iptc
############

This module provides the classes :class:`IptcTag` and :class:`IptcValueError`.

.. class:: pyexiv2.iptc.IptcTag

**Instance Attributes**

..

* :ref:`description <descript>`
* :ref:`key <key1>`
* :ref:`name <name1>`
* :ref:`photoshop_name <photoshopname>`
* :ref:`raw_value <rawvalue1>`
* :ref:`record_description <recorddescription>`
* :ref:`record_name <recordname>`
* :ref:`repeatable <repeatable>`
* :ref:`title <title>`
* :ref:`type <type1>`
* :ref:`value <value1>`

**Description**

The :class:`IptcTag` define an IPTC tag.

**Documentation**

**Instanciation**

.. class:: pyexiv2.iptc.IptcTag(key, value=None, _tag=None)

   An IPTC tag.

   Arguments:

      * *key* The key of the tag in the dotted form *familyName.groupName.tagName* where *familyName* = *iptc*.
      * *value* The value of the tag.

   This tag can have several values (tags that have the *repeatable* property).

   Here is a correspondance table between the IPTC types and the possible python types the value of a tag may take:

       * Short: int
       * String: string
       * Date: :class:`datetime.date`
       * Time: :class:`datetime.time`
       * Undefined: string

**Attributes**

.. _descript:
.. attribute:: description

   The description of the tag.

.. _key1:
.. attribute:: key

   The key of the tag in the dotted form familyName.groupName.tagName where familyName = iptc.

.. _name1:
.. attribute:: name

   The name of the tag (this is also the third part of the key).

.. _photoshopname:
.. attribute:: photoshop_name

   The Photoshop name of the tag

.. _rawvalue1:
.. attribute:: raw_value

   The raw values of the tag as a list of strings.

.. _recorddescription:
.. attribute:: record_description

   The description of the tag’s record.

.. _recordname:
.. attribute:: record_name

   The name of the tag’s record.

.. _repeatable:
.. attribute:: repeatable

   Whether the tag is repeatable (accepts several values).

.. _title:
.. attribute:: title

   The title (label) of the tag.

.. _type1:
.. attribute:: type

   The IPTC type of the tag (one of Short, String, Date, Time, Undefined).

.. _value1:
.. attribute:: value

   The values of the tag as a list of python objects.


.. class:: pyexiv2.iptc.IptcValueError(ValueError)

   Exception raised when failing to parse the value of an IPTC tag.


**Attributes**

.. attribute:: value

   The value that fails to be parsed

.. attribute:: type

   The IPTC type of the tag


pyexiv2.xmp
###########

This module provides the classes :class:`XmpTag` and :class:`XmpValueError` and the following five functions to handle the XMP parser and name spaces.


.. function:: pyexiv2.xmp.initialiseXmpParser()

   Initialise the xmp parser.

   Calling this method is usually not needed, as encode() and decode() will 
   initialize the XMP Toolkit if necessary.

   This function itself still is not thread-safe and needs to be 
   called in a thread-safe manner (e.g., on program startup).


.. function:: pyexiv2.xmp.closeXmpParser()

   Close the xmp parser.

   Terminate the XMP Toolkit and unregister custom namespaces.

   Call this method when the XmpParser is no longer needed to allow the XMP 
   Toolkit to cleanly shutdown.


.. function:: pyexiv2.xmp.register_namespace(name, prefix)

   Register a custom XMP namespace.

   Overriding the prefix of a known or previously registered namespace is not allowed.

   Arguments:

      * *name* str() The name of the custom namespace (ending with a /), typically a URL (e.g. http://purl.org/dc/elements/1.1/)
      * *prefix* str() The prefix for the custom namespace (keys in this namespace will be in the form Xmp.{prefix}.{something})

   Raises:	

      * *ValueError* – if the name doesn’t end with a /
      * *KeyError* – if a namespace already exist with this prefix


.. function:: pyexiv2.xmp.unregister_namespace(name)

   Unregister a custom XMP namespace.

   A custom namespace is identified by its name, not by its prefix.

   Attempting to unregister an unknown namespace raises an error, as does attempting to unregister a builtin namespace.

   Arguments:

      * *name* str() The name of the custom namespace (ending with a /), typically a URL (e.g. http://purl.org/dc/elements/1.1/)

   Raises:	

      * *ValueError* – if the name doesn’t end with a /
      * *KeyError* – if the namespace is unknown or a builtin namespace


.. function:: pyexiv2.xmp.unregister_namespaces()

   Unregister all custom XMP namespaces.

   Builtin namespaces are not unregistered.

   This function always succeeds.


.. class:: pyexiv2.xmp.XmpTag

**Instance Attributes**

..

* :ref:`description <description2>`
* :ref:`key <key2>`
* :ref:`name <name2>`
* :ref:`raw_value <raw_value2>`
* :ref:`title <title2>`
* :ref:`type <type2>`
* :ref:`value <value2>`

**Description**

The :class:`XmpTag` define an XMP tag.

**Documentation**

**Instanciation**

.. class:: pyexiv2.xmp.XmpTag(key, value=None, _tag=None)

   An XMP tag.

   Arguments:

      * *key* The key of the tag in the dotted form *familyName.groupName.tagName* where *familyName* = *xmp*.
      * *value* The value of the tag.

   Here is a correspondance table between the XMP types and the possible python types the value of a tag may take:

      * alt, bag, seq: list of the contained simple type
      * lang alt: dict of (language-code: value)
      * Boolean: boolean
      * Colorant: *[not implemented yet]*
      * Date: :class:`datetime.date`, :class:`datetime.datetime`
      * Dimensions: *[not implemented yet]*
      * Font: *[not implemented yet]*
      * GPSCoordinate: :class:`pyexiv2.utils.GPSCoordinate`
      * Integer: int
      * Locale: *[not implemented yet]*
      * MIMEType: 2-tuple of strings
      * Rational: :class:`fractions.Fraction`
      * Real: *[not implemented yet]*
      * AgentName, ProperName, Text: unicode string
      * Thumbnail: *[not implemented yet]*
      * URI, URL: string
      * XPath: *[not implemented yet]*

**Attributes**

.. _description2:
.. attribute:: description

   The description of the tag.

.. _key2:
.. attribute:: key

   The key of the tag in the dotted form familyName.groupName.tagName where familyName = xmp.

.. _name2:
.. attribute:: name

   The name of the tag (this is also the third part of the key).

.. _raw_value2:
.. attribute:: raw_value

   The raw value of the tag as a [list of] string(s).

.. _title2:
.. attribute:: title

   The title (label) of the tag.

.. _type2:
.. attribute:: type

   The XMP type of the tag.

.. _value2:
.. attribute:: value

   The value of the tag as a [list of] python object(s).


.. class:: pyexiv2.xmp.XmpValueError(ValueError)

   Exception raised when failing to parse the value of an XMP tag.


**Attributes**

.. attribute:: value

   The value that fails to be parsed

.. attribute:: type

   The XMP type of the tag


pyexiv2.preview
###############

.. class:: pyexiv2.preview.Preview

**Instance Attributes**

..

* :ref:`dimensions <dimensions1>`
* :ref:`extension <extension1>`
* :ref:`mime_type <mime_type1>`
* :ref:`size <size>`
* :ref:`data <data1>`


**Instance Method**

..

* :ref:`write_to_file(path) <write-to-file>`

**Description**

The :class:`Preview` define a preview image (properties and data buffer) embedded in image metadata.

**Documentation**

**Instanciation**

.. class:: pyexiv2.preview.Preview(preview)

    A preview image embedded in image metadata.

**Attributes**

.. _dimensions1:
.. attribute:: dimensions

      A tuple containing the width and height of the preview image in pixels.

.. _extension1:
.. attribute:: extension

      The file extension of the preview image with a leading dot (e.g. .jpg).

.. _mime_type1:
.. attribute:: mime_type

      The mime type of the preview image (e.g. image/jpeg).

.. _size:
.. attribute:: size

      The size of the preview image in bytes.

.. _data1:
.. attribute:: data

   The preview data as a Python list. The data can be send to an image library.

   *New in version 0.6.0*

   Example with Pillow::

   >>> from PIL import Image
   >>> import io
   >>> from pyexiv2 import ImageMetadata, exif
   >>> meta = ImageMetadata("lena.jpg")
   >>> meta.read()
   >>> # try with the first one
   >>> preview = meta.previews[0]
   >>> byteio = io.BytesIO(preview.data)
   >>> img = Image.open(byteio)
   >>> img.show()

**Method**

.. _write-to-file:
.. function:: write_to_file(path)
    
      Write the preview image to a file on disk. The file extension will be automatically appended to the path.

      Argument:	

         * *path* str(path) The file path to write the preview to (without an extension)


