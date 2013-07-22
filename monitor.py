from celery import Celery

BROKER_URL = "amqp://celery:celery@master2.htfs.info:5672//celery"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks.monitor",)

celery = Celery(broker=BROKER_URL)