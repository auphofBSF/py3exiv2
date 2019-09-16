Developers
==========

If you are a developer and use py3exiv2 in your project, you will find here
useful information.

Getting the code
################

py3exiv2's source code is versioned with
`bazaar <http://bazaar.canonical.com/>`_, and the main development focus (sometimes referred to as *trunk*), is hosted on `Launchpad <https://code.launchpad.net/py3exiv2>`_.

To get a working copy of the latest revision of the development branch, just
issue the following command in a terminal::

  bzr branch lp:py3exiv2

Dependencies
############

To use py3exiv2:

* `Python <http://python.org/download/>`_ ≥ 3.2
* `boost.python <http://www.boost.org/libs/python/doc/>`_ ≥ 1.46
* `libexiv2 <http://exiv2.org/>`_ ≥ 0.20

To build py3exiv2:

* `python-all-dev` (≥ 3.2)
* `libexiv2-dev` (≥ 0.20)
* `libboost-python-dev` (≥ 1.45)
* `g++`

Some unit tests have a dependency on
`python-tz <http://pytz.sourceforge.net/>`_.
This dependency is optional: the corresponding tests will be skipped if it is
not present on the system.

Additionally, if you want to cross-compile py3exiv2 for Windows and generate a
Windows installer, you will need the following dependencies:

* `MinGW <http://www.mingw.org/>`_
* `7-Zip <http://7-zip.org/>`_
* `NSIS <http://nsis.sourceforge.net/>`_

Building and installing
#######################

Linux
+++++

Open a terminal into the top-level directory (where is the file *configure.py*)::

  $ python3 configure.py

The configure script try to find the exact name of `libboost_python3` wich is depending on your environment. If it can't find the lib, give it the full path of this lib with the option *--libboost*. Example on Debian with Python-3.4::

  $ python3 configure.py --libboost=/usr/lib/x86_64-linux-gnu/libboost_python-py34.so

Build the lib::

  $ ./build.sh

The result of the build process is a shared library, ``libexiv2python.so``, in the build directory::

  $ ls build/
  $ exiv2wrapper.os  exiv2wrapper_python.os  libexiv2python.so

And, if no error, install all the files::

  $ ./build.sh -i

You will most likely need administrative privileges to the last step.


Documentation
#############

The present documentation is generated using
`Sphinx <http://sphinx.pocoo.org/>`_ from reStructuredText sources found in the
doc/ directory. Invoke ``make html`` to (re)build the HTML documentation.

The index of the documentation will then be found under doc/_build/html/index.html.

Unit tests
##########

py3exiv2's source comes with a battery of unit tests, in the test/ directory.
To run them, invoke ``python3 TestsRunner.py``.

Contributing
############

py3exiv2 is Free Software, meaning that you are encouraged to use it, modify it
to suit your needs, contribute back improvements, and redistribute it.

`Bugs <https://bugs.launchpad.net/py3exiv2>`_ are tracked on Launchpad.
There is a team called
`py3exiv2-developers <https://launchpad.net/~py3exiv2-team>`_ open to anyone
interested in following development on py3exiv2. Don't hesitate to subscribe to
the team (you don't need to actually contribute!) and to the associated mailing
list.

There are several ways in which you can contribute to improve py3exiv2:

* Use it;
* Give your feedback and discuss issues and feature requests on the
  mailing list;
* Report bugs, write patches;
* Package it for your favorite distribution/OS.

When reporting a bug, don't forget to include the following information in the
report:

* version of py3exiv2
* version of libexiv2 it was compiled against
* a minimal script that reliably reproduces the issue
* a sample image file with which the bug can reliably be reproduced

