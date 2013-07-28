from yaml import load
from celery.task import task

@task(name='planner.get_model_data')
def get_model_data(config):
	
    return config.plans