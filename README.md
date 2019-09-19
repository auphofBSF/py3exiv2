# py3exiv2
*******

Welcome to py3exiv2, a python 3 binding to exiv2 (http://exiv2.org/), the C++
library for manipulation of EXIF, IPTC and XMP image metadata.
It is a python 3 module that allows your python scripts to read and write
metadata (EXIF, IPTC, XMP, thumbnails) embedded in image files
(JPEG, TIFF, ...).

Point your browser to http://exiv2.org/metadata.html for the complete metadata
tag reference.

This fork supporting  Windows is based on the suggestions by in a post by the author, Vincent Vande Vyvre
https://www.developpez.net/forums/d1971475/autres-langages/python/deploiement-installation/py3exiv2-installation-sous-windows/#post10935110
and the GithubGist  [py3exiv2 patched setup.py file for installation on Windows using vcpkg ](https://gist.github.com/ksdme/190f91b33ca1138b0ff85ab662c02e6a) by https://github.com/ksdme

TODO: further improve the setup to automatically build/install boost on windows

==================

py3exiv2 depends on the following libraries:

 * python (≥ 3.3)
 * boost.python3 (http://www.boost.org/libs/python/doc/index.html)
 * exiv2 (http://www.exiv2.org/)

Some examples in src/ use PyGTK (http://www.pygtk.org/) and PyQt
(http://www.riverbankcomputing.co.uk/software/pyqt/) to display image previews,
those are optional dependencies.

This is a typical list of build dependencies for a Debian/Ubuntu system:

 * python-all-dev (≥ 3.3)
 * libexiv2-dev (≥ 0.20)
 * libboost-python-dev (≥ 1.48)
 * g++


Building and installing
=======================

## Linux

To build and install the library, while in the top-level directory
(e.g. '~/dev/p3yexiv2', which should contain a file named 'configure.py'),
run the following commands:

 $ python3 configure.py     # To chek your environment and write the Makefile
 $ ./build.sh               # To compile the lib
 $ ./build.sh -i            # as administrator to install all files

You can run configure.py with the following arguments:
    -h                  show the help message and exit
    --libboost=FILE     where FILE is the full path of libboost-python3
                        e.g. `/usr/lib/x86_64-linux-gnu/libboost_python-py34.so`

The result of the build is a dynamic library, libexiv2python.so, in the build/
directory. This is the low-level binding. It is in turn used in a higher level
module, pyexiv2.
The `./build.sh -i` command installs the two modules in your site-specific directory
for Python modules (e.g. '/usr/lib/python3/dist-packages/' on Linux).

To use py3exiv2 in your scripts, simply import the pyexiv2 module.

Note: the lib name is py3exiv2 but, for compatibility, the top-level module 
      is named pyexiv2


## Windows 10

The installation is more complex but following guidelines by
https://www.developpez.net/forums/u263817/vinss/ 
as discussed in https://www.developpez.net/forums/d1971475/autres-langages/python-zope/deploiement-installation/py3exiv2-installation-sous-windows/ there is now a windows .bat file.

### INSTALLING PYEXIV3 ON WINDOWS for a particular version of Python
- install GIT-2.21.0-64-bit.exe
- install VSCodeUserSetup-x64-1.33.1.exe
- configure vcpkg ports of python3 for the correct python major.minor.patch version by editing the `vcpkg_custom\ports\python3` files CONTROL and portfile.cmake.
- change directory to `cd windows-vcpkg` 
- edit vcpkgSetup.bat to define the install point for **vcpkg** then execute the automated setup `vcpkgSetup.bat`

the proceed to install with pip
- set path to find the vcpkg built dependincies
  `set PATH=%VCPKG%\install\x64-windows\bin;%PATH%`
  
- Now Install py3exiv2 `pip install -e <dir of py3exiv2\setup.py>`


For future execution of python code using py3exiv2  add the dependency paths for the boost 
```
set VCPKG=<<your installed path for vcpkg>>
set PATH=%VCPKG%\installed\x64-windows\bin;%PATH%
```


Documentation
=============

You can find the API documentation at: 
    http://python3-exiv2.readthedocs.org/en/latest
or refer to the internal documentation for a guide on how to use py3exiv2.
In a python interpreter, type:

 >>> import pyexiv2
 >>> help(pyexiv2)


License
=======

Copyright (C) 2006-2011 Olivier Tilloy <olivier@tilloy.net>
Copyright (C) 2015-2019 Vincent Vande Vyvre <vincent.vandevyvre@oqapy.eu>

py3exiv2 is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License version 3 as published by the Free
Software Foundation.

py3exiv2 is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with py3exiv2; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, 5th Floor, Boston, MA 02110-1301 USA.


Developers
==========

py3exiv2 is Free Software, meaning that you are encouraged to play with it,
modify it to suit your needs and contribute back your changes and bug fixes.

The bug tracking system and the main bazaar branch are hosted at Launchpad:

 https://launchpad.net/py3exiv2

To get a working copy of the latest version of the code, you need to have bazaar
(http://bazaar.canonical.com/) installed:

 $ bzr branch lp:py3exiv2

Feedback, bug reports and patches are welcome!


