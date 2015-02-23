from __future__ import absolute_import

from celery import Celery

app = Celery('monitor')

from robotice import worker_monitor

app.config_from_object(worker_monitor)