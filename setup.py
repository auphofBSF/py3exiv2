#! / Usr / bin / python3
# - * - coding: utf-8 - * -
# Replacement setup.py for py3exiv2, that allows building on windows using VCPKG see Readme
# THis py3exiv2 implementation of pyexiv2 is Forked from rev105 : https://bazaar.launchpad.net/~vincent-vandevyvre/py3exiv2/trunk/files/105
# based on the suggestions by in a post by the author, Vincent Vande Vyvre
# https://www.developpez.net/forums/d1971475/autres-langages/python/deploiement-installation/py3exiv2-installation-sous-windows/#post10935110
# and the GithubGist  [py3exiv2 patched setup.py file for installation on Windows using vcpkg ](https://gist.github.com/ksdme/190f91b33ca1138b0ff85ab662c02e6a) by https://github.com/ksdme
# 
# TODO: further improve the setup to automatically build/install boost on windows


import sys
import os
import glob
import subprocess

from setuptools import setup, find_packages, Extension

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

def get_libboost_name():
    """
    Returns the name of the lib libboost_python 3
    """
    places = ('/usr/lib/', '/usr/local/lib/', '/usr/')
    for place in places:
        cmd = ['find', place, '-name', 'libboost_python*']
        rep = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
        if not rep:
            continue

        # rep is type bytes
        libs = rep.decode(sys.getfilesystemencoding()).split('\n')
        for l in libs:
            _, l = os.path.split(l)
            if '.so' in l:
                l = l.split('.so')[0]
                # Assume there's no longer python2.3 in the wild
                if '3' in l[-2:]:
                    return l.replace('libboost', 'boost')

if os.name == 'nt':
    basep = os.environ["VCPKG"] + r"\installed\x64-windows"

    py_version = "{}{}".format(sys.version_info.major,sys.version_info.minor)
    os.environ["INCLUDE"] = basep + r"\include"
    libboost = basep + r"\lib\boost_python"+py_version+r"-vc140-mt"
    libexiv = basep + r"\lib\exiv2"
    extra_compile_args = []
else:
    libboost = get_libboost_name()
    extra_compile_args = []
    libexiv = 'exiv2'

setup(
    name='py3exiv2',
    version='0.7.2RCwinX64',
    description='A Python3 binding to the library exiv2',
    long_description=long_description,
    url='https://launchpad.net/py3exiv2',
    author='Vincent Vande Vyvre',
    author_email='vincent.vandevyvre@oqapy.eu',
    license='GPL-3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: C++',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    keywords='exiv2 pyexiv2 EXIF IPTC XMP image metadata',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    package_data={'':['src/*.cpp', 'src/*.hpp',]},
    #cmdclass={'install': install},
    ext_modules=[
    Extension('libexiv2python',
        ['src/exiv2wrapper.cpp', 'src/exiv2wrapper_python.cpp'],
        include_dirs=[],
        library_dirs=[],
        libraries=[libboost, libexiv],
        extra_compile_args=extra_compile_args)
    ],
)