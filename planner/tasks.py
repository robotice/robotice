from yaml import load
from celery.task import task

logger = get_task_logger(__name__)

@task(name='planner.get_model_data')
def get_model_data(config):
	logger.info(config)
    return config.plans