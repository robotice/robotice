from datetime import timedelta
from kombu import Queue, Exchange
from celery import Celery
import logging

from conf import setup_app
from conf.celery import *

LOG = logging.getLogger(__name__)

config = setup_app('monitor')

BROKER_URL = config.broker

if "amqp" in config.broker:

    default_exchange = Exchange('default')
    monitor_exchange = Exchange('monitor', type='fanout')

    CELERY_RESULT_BACKEND = "amqp"
    CELERY_QUEUES = (
        Queue('default', default_exchange, routing_key='default'),
        Queue('monitor', monitor_exchange, routing_key='monitor_%s' % config.hostname),
    )

elif "redis" in config.broker:

    CARROT_BACKEND = "redis"
    CELERY_RESULT_BACKEND = BROKER_URL
    #BROKER_TRANSPORT_OPTIONS = {
    #    'visibility_timeout': 3600, 'fanout_prefix': True}
    CELERY_QUEUES = {
        "default": {"default": "default"},
        'monitor': {'monitor_%s' % config.hostname: "monitor.#"},
    }

CELERY_IMPORTS = (
    "monitor.tasks",
)


CELERY_ROUTES = {
    'reasoner.process_real_data': {
        'queue': 'reasoner',
    },
    'monitor.get_sensor_data': {
        'queue': 'monitor_%s' % config.hostname,
    },
    'monitor.return_sensor_data': {
        'queue': 'monitor',
    },
}