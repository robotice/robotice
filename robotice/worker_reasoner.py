
from __future__ import absolute_import
import logging

from datetime import timedelta


from robotice.conf import RoboticeSettings

from robotice.conf.celery import *

LOG = logging.getLogger(__name__)

config = RoboticeSettings('reasoner')

BROKER_URL = config.broker


if "amqp" in config.broker:
    from kombu import Queue, Exchange
    CELERY_RESULT_BACKEND = "amqp"

    default_exchange = Exchange('default')
    monitor_exchange = Exchange('reasoner', type='fanout')

    CELERY_QUEUES = (
        Queue('default', default_exchange, routing_key='default'),
        Queue('reasoner', control_exchange, routing_key='reasoner.#'),
    )

elif "redis" in config.broker:
    CARROT_BACKEND = "redis"
    CELERY_RESULT_BACKEND = BROKER_URL
    # 1 hour.
    #BROKER_TRANSPORT_OPTIONS = {
    #    'visibility_timeout': 3600, 'fanout_prefix': True}
    CELERY_QUEUES = {
        "default": {"default": "default"},
        "reasoner": {"reasoner": "reasoner.#"},
    }

CELERY_IMPORTS = ("robotice.reasoner.tasks",)


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
    'reasoner.process_real_data': {
        'queue': 'reasoner',
    },
    'reactor.commit_action': {
        'queue': 'reactor',
    }
}

CELERYBEAT_SCHEDULE = {
    'compare-data': {
        'task': 'reasoner.compare_data',
        'schedule': timedelta(seconds=60),
        'args': (config, ),
    },
    'real-data-reader': {
        'task': 'monitor.get_real_data',
        'schedule': timedelta(seconds=60),
        'args': (config, ),
    },
    'planned-data-reader': {
        'task': 'planner.get_model_data',
        'schedule': timedelta(seconds=60),
        'args': (config, ),
    },
}

