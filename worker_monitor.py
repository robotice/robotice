from datetime import timedelta
from kombu import Queue, Exchange
from celery import Celery
import logging

from utils import setup_app

config = setup_app()

logger = logging.getLogger("robotice.monitor")

BROKER_URL = config.broker
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = (
	"monitor.tasks",
)

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
    'real-data-reader': {
        'task': 'monitor.get_real_data',
        'schedule': timedelta(seconds=5),
        'args': (config, ),
    },
}

celery = Celery(broker=BROKER_URL)
