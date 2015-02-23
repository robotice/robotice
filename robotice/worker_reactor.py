
from __future__ import absolute_import

from kombu import Queue, Exchange

from robotice.conf import setup_app
from robotice.conf.celery import *

config = setup_app('reactor')

BROKER_URL = config.broker

if "amqp" in config.broker:

    default_exchange = Exchange('default')
    reactor_exchange = Exchange('reactor', type='fanout')
    CELERY_RESULT_BACKEND = "amqp"
    CELERY_QUEUES = (
        Queue('default', default_exchange, routing_key='default'),
        Queue('reactor', reactor_exchange, routing_key='reactor.#'),
    )

elif "redis" in config.broker:
    CELERY_RESULT_BACKEND = BROKER_URL
    #BROKER_TRANSPORT_OPTIONS = {
    #    'visibility_timeout': 3600, 'fanout_prefix': True}
    CELERY_QUEUES = {
        "default": {"default": "default"},
        "reactor": {"reactor": "reactor.#"},
    }

CELERY_IMPORTS = (
    "robotice.reactor.tasks",
)

CELERY_ROUTES = {
    'monitor.get_real_data': {
        'queue': 'monitor',
    },
    'planner.get_model_data': {
        'queue': 'planner',
    },
    'reasoner.compare_data': {
        'queue': 'reasoner',
    },
    'reactor.commit_action': {
        'queue': 'reactor',
    }
}

#celery = Celery('reactor', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)