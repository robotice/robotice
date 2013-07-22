
from celery.task import task
 
@task
def get_data(sensor):

    return ['metrics.value', 24]