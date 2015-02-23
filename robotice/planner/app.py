from __future__ import absolute_import

from celery import Celery

app = Celery('planner')

from robotice import worker_planner

app.config_from_object(worker_planner)