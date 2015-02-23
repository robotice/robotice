from __future__ import absolute_import

from celery import Celery

app = Celery('reasoner')

from robotice import worker_reasoner

app.config_from_object(worker_reasoner)