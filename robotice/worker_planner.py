
import logging

from datetime import timedelta
from kombu import Queue, Exchange
from celery import Celery

from conf import setup_app
from conf.celery import *

LOG = logging.getLogger(__name__)

config = setup_app('planner')

BROKER_URL = config.broker

if "amqp" in config.broker:

    default_exchange = Exchange('default')
    planner_exchange = Exchange('planner', type='fanout')
    CELERY_RESULT_BACKEND = "amqp"
    CELERY_QUEUES = (
        Queue('default', default_exchange, routing_key='default'),
        Queue('planner', planner_exchange, routing_key='planner.#'),
    )

elif "redis" in config.broker:

    CARROT_BACKEND = "redis"
    CELERY_RESULT_BACKEND = BROKER_URL
    #BROKER_TRANSPORT_OPTIONS = {
    #    'visibility_timeout': 3600, 'fanout_prefix': True}
    CELERY_QUEUES = {
        "default": {"default": "default"},
        "planner": {"planner": "planner.#"},
    }

CELERY_RESULT_EXCHANGE = 'results'
CELERY_RESULT_EXCHANGE_TYPE = 'fanout'
CELERY_TASK_RESULT_EXPIRES = 300

CELERY_IMPORTS = (
    "planner.tasks",
)


CELERY_ROUTES = {
    'planner.get_model_data': {
        'queue': 'planner',
    },
    'planner.return_model_data': {
        'queue': 'planner',
    },
}