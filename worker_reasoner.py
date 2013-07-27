from datetime import timedelta

from kombu import Queue, Exchange
from celery import Celery
from celery.execute import send_task
from celery.schedules import crontab

from utils import setup_app

config = setup_app()

BROKER_URL = config.broker
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("reasoner.tasks", "monitor.tasks", "reactor.tasks", "planner.tasks")

default_exchange = Exchange('default', type='direct')
monitor_exchange = Exchange('monitor', type='direct')
reactor_exchange = Exchange('reactor', type='direct')
planner_exchange = Exchange('planner', type='direct')

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
#        'routing_key': 'monitor.get_real_data',
    },
    'monitor.return_real_data': {
        'queue': 'monitor',
#        'routing_key': 'monitor.return_real_data',
    },
    'monitor.get_sensor_data.dht': {
        'queue': 'monitor',
#        'routing_key': 'monitor.get_sensor_data.dummy',
    },
    'monitor.get_sensor_data.dummy': {
        'queue': 'monitor',
#        'routing_key': 'monitor.get_sensor_data.dummy',
    },
    'monitor.get_sensor_data.sispm': {
        'queue': 'monitor',
#        'routing_key': 'monitor.get_sensor_data.dummy',
    },
    'planner.get_model_data': {
        'queue': 'planner',
#        'routing_key': 'planner.get_model_data',
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
        'schedule': timedelta(seconds=5),
        'args': (config, ),
    },
}

celery = Celery(broker=BROKER_URL)

