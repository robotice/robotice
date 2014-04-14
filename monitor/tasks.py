from time import time
import decimal

from celery import group, chord
from celery.task import task
from celery.utils.log import get_task_logger

from reasoner.tasks import process_real_data

from utils import get_grains

logger = get_task_logger(__name__)

@task(name='monitor.get_real_data')
def get_real_data(config):

    tasks = []

    grains = get_grains()

    for sensor in config.sensors:
        tasks.append(get_sensor_data.subtask((sensor,), exchange='monitor_%s' % config.hostname))

    job = group(tasks)

    result = job.apply_async(link=process_real_data.subtask((config, ), exchange='reasoner'))

    return 0 #'Started reading real data from sensors %s on device %s at %s' % (config.sensors, config.hostname, time())

@task(name='monitor.get_sensor_data', track_started=True)
def get_sensor_data(sensor):

    sensor_module = __import__(".".join(["sensors", sensor.device],))
    logger.info('Reading sensor: %s' % sensor)
    return sensor_module.get_data(sensor)
