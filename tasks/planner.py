
from celery.task import task
 
@task
def get_model():

    return 0


@task
def get_model_values(timestamp):

    return 0