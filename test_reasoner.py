from celery import Celery
from yaml import load

from celery.execute import send_task
from celery.schedules import crontab

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

BROKER_URL = config.get('broker')

celery = Celery(broker=BROKER_URL)

CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks.reasoner", "tasks.monitor", "tasks.reactor", "tasks.planner")

#celery.config_from_object(Config)

from tasks.reasoner import maintain_system

print '1'

result = maintain_system.delay(config).get()

print result
