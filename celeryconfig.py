from yaml import load
from kombu import Queue
from celery import Celery

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

BROKER_URL = config.get('broker')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("planner.tasks", "monitor.tasks", "reactor.tasks")

CELERY_DEFAULT_QUEUE = 'default'

CELERY_QUEUES = (
    Queue('default', routing_key='default.#'),
    Queue('monitor', routing_key='monitor.#'),
    Queue('planner', routing_key='planner.#'),
)
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default.task'

CELERY_TIMEZONE = 'UTC'

CELERY_ROUTES = {
    'monitor.get_real_data': {
        'queue': 'monitor',
#        'routing_key': 'monitor.get_real_data',
    },
    'monitor.return_real_data': {
        'queue': 'monitor',
#        'routing_key': 'monitor.get_real_data',
    },
    'monitor.get_sensor_data.dummy': {
        'queue': 'monitor',
    },
    'monitor.get_sensor_data.sispm': {
        'queue': 'monitor',
    },
    'planner.get_model_data': {
        'queue': 'planner',
        'routing_key': 'planner.get_model_data',
    },
}

celery = Celery(broker=BROKER_URL)