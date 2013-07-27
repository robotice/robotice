from datetime import timedelta

from kombu import Queue

from celery import Celery
from celery.execute import send_task
from celery.schedules import crontab

from utils import setup_app

config = setup_app()

BROKER_URL = config.broker
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("reasoner.tasks", "monitor.tasks", "reactor.tasks", "planner.tasks")
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULE = {
    'system-maintainer': {
        'task': 'reasoner.maintain_system',
        'schedule': crontab(),
        'args': (config, ),
    },
    'data-reader': {
        'task': 'monitor.get_real_data',
        'schedule': timedelta(seconds=10),
        'args': (config, ),
    },
}
"""

        'queue': 'monitor',
        'routing_key': 'monitor.get_real_data'

CELERY_DEFAULT_QUEUE = 'default'

CELERY_QUEUES = (
    Queue('default',    routing_key='default.#'),
    Queue('monitor', routing_key='monitor.#'),
    Queue('planner', routing_key='planner.#'),
)
CELERY_DEFAULT_EXCHANGE = 'tasks'
CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
CELERY_DEFAULT_ROUTING_KEY = 'default.task'
CELERY_ROUTES = {
    'monitor.get_real_data': {
        'queue': 'monitor',
        'routing_key': 'monitor.get_real_data',
    },
    'planner.get_model_data': {
        'queue': 'planner',
        'routing_key': 'planner.get_model_data',
    },
}
""" 
celery = Celery(broker=BROKER_URL)

