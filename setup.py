#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Replacement setup.py for py3exiv2, that allows building on OSX
# https://gist.github.com/ndevenish/6410cab393bd8dec1b016061ddb5573b

import sys
import os
import glob
import subprocess
import platform

from setuptools import setup, find_packages, Extension

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

def get_libboost_osx():
    places = ["/usr/local/lib/"]
    for place in places:
        lib = place + "libboost_python3*.dylib"
        files = glob.glob(lib)
        for f in files:
            if not "-mt" in f:
                return os.path.basename(f).replace("lib", "").split(".")[0]
            
        print("NOT FOUND", files)
        sys.exit()
    
if platform.system() == "Darwin":
    boostlib = get_libboost_osx()
    print(boostlib)

else:
    boostlib = 'boost_python3'

setup(
    name='py3exiv2',
    version='0.7.1',
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
        libraries=[boostlib, 'exiv2'],
        extra_compile_args=['-g']
        )
    ],
)

