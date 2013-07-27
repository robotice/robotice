from datetime import timedelta
from celery import Celery
from yaml import load
import logging

config_file = open("/srv/robotice/config.yml", "r")
config = load(config_file)

logger = logging.getLogger("robotice.monitor")

BROKER_URL = config.get('broker')
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = (
	"monitor.tasks",
)

celery = Celery(broker=BROKER_URL)
