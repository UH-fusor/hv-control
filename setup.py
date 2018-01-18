#!/usr/bin/env python3

# Always prefer setuptools over distutils
from setuptools import setup
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='technix',
    version='0.0.1',
    description='Serial control for Technix SR PSUs',
    long_description=long_description,
    url='https://github.com/UH-fusor/hv-control',
    author='University of Helsinki',
    author_email='fusor-team@helsinki.fi',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        ],
    keywords='serial rs232 technix control high_voltage',
    py_modules=['technix'],
    install_requires=['pyserial'],
    package_dir={'':'lib'}
)
