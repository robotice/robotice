from yaml import load
from celery.task import task

logger = get_task_logger(__name__)

@task(name='planner.get_model_data')
def get_model_data(config):
    return config.plans

@task(name='planner.return_model_data')
def return_model_data(config):
    return config.plans