
from celery.task import task
from yaml import load

@task
def get_model():
    config_file = open("/srv/robotice/config.yml", "r")
    return load(config_file)

@task
def get_model_values(timestamp):

    return 0