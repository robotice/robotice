from __future__ import absolute_import

from celery import Celery

app = Celery('reactor')

from robotice import worker_reactor

app.config_from_object(worker_reactor)