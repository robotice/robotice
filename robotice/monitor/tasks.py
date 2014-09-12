import os
from time import time
import decimal
import subprocess

from celery import group, chord
from celery.task import task
from celery.execute import send_task
from celery.utils.log import get_task_logger

from robotice.conf import setup_app
from utils.functional import import_module

logger = get_task_logger(__name__)


@task(name='monitor.get_real_data')
def get_real_data(config):

    tasks = []
    logger = get_real_data.get_logger()
    logger.info('Sensors {0}'.format(config.sensors))

    for sensor in config.sensors:
        tasks.append(get_sensor_data.subtask(
            (config, sensor), exchange='monitor_%s' % config.hostname))
        logger.info('Registred get_sensor_data {0}'.format(sensor))

    job = group(tasks)
    result = job.apply_async()

    return 'Started reading real data from sensors %s on device %s at %s' % (config.sensors, config.hostname, time())


@task(name='monitor.get_sensor_data', track_started=True)
def get_sensor_data(config, sensor):

    LOG = get_real_data.get_logger()

    result = None

    try:
        mod = import_module(sensor.get("device"))
    except Exception, e:
        LOG.error("Cannot import sensor %s" % sensor)
        raise e

    results = mod.get_data(sensor)

    LOG.debug("sensor: {0} result: {0}".format(sensor, results))

    send_task("reasoner.process_real_data",
              args=(results, sensor))

    LOG.debug(
        'Registred process_real_data for {0}'.format(sensor.get("name")))

    result = 'Real data from sensor %s on device %s results %s' % (sensor.get("name"), config.hostname, results)

    return result
