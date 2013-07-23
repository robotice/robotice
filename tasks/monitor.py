
from celery import group
from celery.task import task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@task(name='monitor.get_real_data')
def get_real_data(sensors):

    tasks = []

    for sensor in sensors:
        if sensor.get("type") == "dht":
            tasks.append(dht_get_data.subtask((sensor,)))
        elif sensor.get("type") == "sispm":
            tasks.append(sispm_get_data.subtask((sensor,)))
        elif sensor.get("type") == "dummy":
            tasks.append(dummy_get_data.subtask((sensor,)))
   
    logger.info('Doing %s tasks' % tasks)
    logger.info('Sensors: %s' % sensors)

    job = group(tasks)
    result = job.apply_async()

    return result.join()

@task(name='monitor.collect_real_data')
def collect_real_data(results, tasks):

    completed_tasks = []
    for task in tasks:
        if task.ready():
            completed_tasks.append(task)
            results.append(task.get())

    # remove completed tasks
    tasks = list(set(tasks) - set(completed_tasks))

    logger.info('%s tasks to do' % len(tasks))

    if len(tasks) > 0:
        # resend the task to execute at least 1 second from now
        collect_real_data.delay(results, tasks, countdown=1)
    else:
        # we done
        return results

from sensors.dht import get_dht_data

@task(name='monitor.dht.get_data')
def dht_get_data(sensor):

    logger.info('Reading sensor: %s' % sensor)

    return ['metrics.value', 24]

from sensors.dummy import get_dummy_data

@task(name='monitor.dummy.get_data')
def dummy_get_data(sensor):

    logger.info('Reading sensor: %s' % sensor)

    return ['metrics2.value', 14]

from sensors.sispm import get_sispm_data

@task(name='monitor.sispm.get_data')
def get_sispm_data(sensor):

    logger.info('Reading sensor: %s' % sensor)

    return ['metrics3.value', 2543]
