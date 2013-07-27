
from celery.task import task
from yaml import load

@task(name='planner.get_model')
def get_model():
    config_file = open("/srv/robotice/config.yml", "r")

    return load(config_file)

@task(name='planner.get_model_data')
def get_model_data(model):

    return 0