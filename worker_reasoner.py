from datetime import timedelta

from kombu import Queue, Exchange
from celery import Celery
from celery.execute import send_task
from celery.schedules import crontab

from utils import setup_app

config = setup_app('reasoner')

BROKER_URL = config.broker
CELERY_RESULT_BACKEND = "amqp"
CELERY_RESULT_EXCHANGE = 'results'
CELERY_RESULT_EXCHANGE_TYPE = 'fanout'
CELERY_TASK_RESULT_EXPIRES = 300

CELERY_IMPORTS = ("reasoner.tasks", "monitor.tasks", "reactor.tasks", "planner.tasks")

default_exchange = Exchange('default', type='fanout')
monitor_exchange = Exchange('monitor', type='fanout')
reactor_exchange = Exchange('reactor', type='fanout')
planner_exchange = Exchange('planner', type='fanout')

CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('monitor', monitor_exchange, routing_key='monitor.#'),
    Queue('planner', planner_exchange, routing_key='planner.#'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default'

CELERY_TIMEZONE = 'UTC'

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
}

CELERYBEAT_SCHEDULE = {
    'system-maintainer': {
        'task': 'reasoner.maintain_system',
        'schedule': crontab(),
        'args': (config, ),
    },
    'real-data-reader': {
        'task': 'monitor.get_real_data',
        'schedule': timedelta(seconds=30),
        'args': (config, ),
    },
    'planned-data-reader': {
        'task': 'planner.get_model_data',
        'schedule': timedelta(seconds=30),
        'args': (config, ),
    },
}

celery = Celery('robotice', broker=BROKER_URL)
