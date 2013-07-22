
from celery.task import task
 
@task
def commit_action(actuator):

    return 0