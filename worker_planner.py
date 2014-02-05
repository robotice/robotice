from datetime import timedelta
from kombu import Queue, Exchange
from celery import Celery
from utils import setup_app

config = setup_app('planner')

BROKER_URL = config.broker
CELERY_RESULT_BACKEND = "amqp"
CELERY_RESULT_EXCHANGE = 'results'
CELERY_RESULT_EXCHANGE_TYPE = 'fanout'
CELERY_TASK_RESULT_EXPIRES = 300

CELERY_IMPORTS = (
    "planner.tasks",
)

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
    'planner.get_model_data': {
        'queue': 'planner',
    },
    'planner.return_model_data': {
        'queue': 'planner',
    },
}

celery = Celery(broker=BROKER_URL)