from time import time

from celery import group, chord
from celery.task import task
from celery.utils.log import get_task_logger

from sensors.dht import get_dht_data
from sensors.dummy import get_dummy_data
from sensors.sispm import get_sispm_data

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

    job = group(tasks)

    result = job.apply_async(link=return_real_data.subtask((), ))

    return 'Started reading at %s' % time()

@task(name='monitor.return_real_data')
def return_real_data(results):
    logger.info(results.join())
    return results.join()

@task(name='monitor.dht.get_data')
def dht_get_data(sensor):
    logger.info('Reading sensor: %s' % sensor)
    return get_dht_data(sensor)

@task(name='monitor.dummy.get_data')
def dummy_get_data(sensor):
    logger.info('Reading sensor: %s' % sensor)
    return get_dummy_data(sensor)

@task(name='monitor.sispm.get_data')
def get_sispm_data(sensor):
    logger.info('Reading sensor: %s' % sensor)
    return get_sispm_data(sensor)
