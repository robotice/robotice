#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from pip.req import parse_requirements
from codecs import open  # To use a consistent encoding
from os import path
import sys
import os

here = path.abspath(path.dirname(__file__))

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import robotice

PACKAGE_NAME = 'robotice'
PACKAGE_DIR = 'robotice'
extra = {}

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


install_reqs = parse_requirements(path.join(here, "requirements/default.txt"))

install_requires = [str(ir.req) for ir in install_reqs]

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()
with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as f:
    history = f.read()
with open(path.join(here, 'LICENSE'), encoding='utf-8') as f:
    license = f.read()

setup(
    author='Ales Komarek & Michael Kuty',
    author_email='mail@newt.cz & mail@majklk.cz',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: System :: Software Distribution',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    description='Opensource monitoring, reasoning and acting framework.',
    include_package_data=False,
    install_requires=install_requires,
    packages=find_packages(exclude=['docs', 'tests*']),
    license=license,
    long_description=readme + '\n\n' + history,
    name=PACKAGE_NAME,
    platforms=['any'],
    url='https://github.com/robotice/robotice',
    version=robotice.__version__,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'robotice=robotice.bin.robotice:main',
        ],
    },
    scripts=['robotice/bin/robotice.py'],
    **extra)
