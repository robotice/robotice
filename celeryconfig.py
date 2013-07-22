BROKER_HOST = "master2.htfs.info"
BROKER_PORT = 5672
BROKER_USER = "celery"
BROKER_PASSWORD = "celery"
BROKER_VHOST = "celery"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("tasks.monitor", "tasks.reactor", "tasks.planner")