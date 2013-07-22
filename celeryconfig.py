from yaml import load

from celery import Celery

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

BROKER_URL = config.get('broker')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks.planner", "tasks.monitor", "tasks.reactor")

celery = Celery(broker=BROKER_URL)