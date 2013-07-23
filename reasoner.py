from celery import Celery
from yaml import load

from celery.execute import send_task
from celery.schedules import crontab

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

BROKER_URL = config.get('broker')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks.reasoner", "tasks.monitor", "tasks.reactor", "tasks.planner")
CELERYBEAT_SCHEDULE = {
    'system-maintainer': {
        'task': 'reasoner.maintain_system',
        'schedule': crontab(),
        'args': (config, ),
    },
    'data-reader': {
        'task': 'monitor.get_real_data',
        'schedule': crontab(),
        'args': (config.get('sensors'), ),
    },
}


celery = Celery(broker=BROKER_URL)