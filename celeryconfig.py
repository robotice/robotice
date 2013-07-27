from yaml import load
from kombu import Queue, Exchange
from celery import Celery

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

BROKER_URL = config.get('broker')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = (
    "planner.tasks",
    "monitor.tasks",
    "reactor.tasks"
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

celery = Celery(broker=BROKER_URL)