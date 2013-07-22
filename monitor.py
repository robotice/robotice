from celery import Celery
from yaml import load

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

BROKER_URL = config.get('broker')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks.monitor",)

celery = Celery(broker=BROKER_URL)