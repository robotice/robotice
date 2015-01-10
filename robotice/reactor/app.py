from __future__ import absolute_import

import os
import sys

from os.path import join, dirname, abspath, normpath

path = normpath(join(abspath(dirname(__file__)), '..'))

sys.path.append(join(path, 'lib', 'python2.7', 'site-packages'))

# If ../../robotice/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'robotice', '__init__.py')):
    sys.path.insert(0, possible_topdir)

from celery import Celery

app = Celery('reactor')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
from robotice import worker_reactor

app.config_from_object(worker_reactor)

app.autodiscover_tasks('robotice.reactor')