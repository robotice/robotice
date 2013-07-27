from datetime import timedelta

from kombu import Queue, Exchange
from celery import Celery
from celery.execute import send_task
from celery.schedules import crontab

from utils import setup_app

config = setup_app()

BROKER_URL = config.broker
CELERY_RESULT_BACKEND = "amqp"
CELERY_RESULT_EXCHANGE = 'results'
CELERY_RESULT_EXCHANGE_TYPE = 'fanout'
CELERY_AMQP_TASK_RESULT_EXPIRES = 1800

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
    'monitor.return_real_data': {
        'queue': 'monitor',
    },
    'monitor.get_sensor_data.dht': {
        'queue': 'monitor',
    },
    'monitor.get_sensor_data.dummy': {
        'queue': 'monitor',
    },
    'monitor.get_sensor_data.sispm': {
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
        'schedule': timedelta(seconds=10),
        'args': (config, ),
    },
    'planned-data-reader': {
        'task': 'planner.get_model_data',
        'schedule': timedelta(seconds=10),
        'args': (config, ),
    },
}

celery = Celery(broker=BROKER_URL)
