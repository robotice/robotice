
from celery.task import task
 
@task
def get_real_data(model):

    return ['metrics.value', 24]