#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import robotice

PACKAGE_NAME = 'robotice'
PACKAGE_DIR = 'robotice'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

install_requires = """
python-statsd==1.6.0
PyYAML==3.10
RPi.GPIO>=0.5.3a
celery==3.1.7
flower==0.6.0
pytz==2011k
redis==2.9.0
raven>=5.0.0
celery-with-redis==3.0
oslo.config==1.4.0
Adafruit-BBIO>=0.0.9
""".split()

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    author='Ales Komarek & Michael Kuty',
    author_email='mail@newt.cz & mail@majklk.cz',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Distributed Environment',
        'Framework :: Celery',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    description='Opensource monitoring, reasoning and acting framework.',
    include_package_data=True,
    install_requires=install_requires,
    license=license,
    long_description=readme + '\n\n' + history,
    name=PACKAGE_NAME,
    platforms=['any'],
    url='https://github.com/robotice/robotice',
    version=robotice.__version__,
    zip_safe=False,
)