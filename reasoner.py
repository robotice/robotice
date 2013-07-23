from datetime import timedelta

from celery import Celery
from celery.execute import send_task
from celery.schedules import crontab

from utils import setup_app

config = setup_app()

BROKER_URL = config.get('broker')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks.reasoner", "tasks.monitor", "tasks.reactor", "tasks.planner")
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

celery = Celery(broker=BROKER_URL)

