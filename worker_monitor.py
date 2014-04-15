from datetime import timedelta
from kombu import Queue, Exchange
from celery import Celery
import logging

from utils import setup_app

config = setup_app('monitor')

logger = logging.getLogger("robotice.monitor")

BROKER_URL = config.broker
CELERY_RESULT_BACKEND = "amqp"
CELERY_RESULT_EXCHANGE = 'results'
CELERY_RESULT_EXCHANGE_TYPE = 'fanout'
CELERY_TASK_RESULT_EXPIRES = 300

CELERY_IMPORTS = (
	"monitor.tasks",
)

default_exchange = Exchange('default', type='fanout')
monitor_exchange = Exchange('monitor', type='fanout')
monitor_local_exchange = Exchange('monitor_%s' % config.hostname, type='fanout')
reactor_exchange = Exchange('reactor', type='fanout')
planner_exchange = Exchange('planner', type='fanout')

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml','application/x-python-serialize',]

CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('monitor', monitor_exchange, routing_key='monitor.#'),
    Queue('monitor_%s' % config.hostname, monitor_local_exchange, routing_key='monitor_%s.#' % config.hostname),
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
    'monitor.get_sensor_data': {
        'queue': 'monitor',
    },
    'monitor.get_sensor_data.cds': {
        'queue': 'monitor_%s' % config.hostname,
    },
    'monitor.get_sensor_data.dht': {
        'queue': 'monitor_%s' % config.hostname,
    },
    'monitor.get_sensor_data.dummy': {
        'queue': 'monitor_%s' % config.hostname,
    },
    'monitor.get_sensor_data.sispm': {
        'queue': 'monitor_%s' % config.hostname,
    },
}

celery = Celery('robotice', broker=BROKER_URL)
celery.control.time_limit('monitor.get_sensor_data.cds', soft=60, hard=120, reply=True)
celery.control.time_limit('monitor.get_sensor_data.sispm', soft=60, hard=120, reply=True)
celery.control.time_limit('monitor.get_sensor_data.dht', soft=60, hard=120, reply=True)
celery.control.time_limit('monitor.get_sensor_data', soft=60, hard=120, reply=True)
celery.control.time_limit('monitor.get_real_data', soft=60, hard=120, reply=True)
