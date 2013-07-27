
from celery.task import task
 
@task(name='reactor.commit_action')
def commit_action(actuator):

    return 0