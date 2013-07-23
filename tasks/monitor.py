
from celery.task import task
 
@task(name='monitor.get_real_data')
def get_real_data(model):

    return ['metrics.value', 24]