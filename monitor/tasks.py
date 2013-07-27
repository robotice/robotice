from time import time

from celery import group, chord
from celery.task import task
from celery.utils.log import get_task_logger

from monitor.sensors.dht import get_dht_data
from monitor.sensors.dummy import get_dummy_data
from monitor.sensors.sispm import get_sispm_data
from monitor.sensors.cds import get_cds_data
                                                
logger = get_task_logger(__name__)

@task(name='monitor.get_real_data')
def get_real_data(config):

    tasks = []

    for sensor in config.sensors:
        if sensor.get("type") == "dht":
            tasks.append(dht_get_data.subtask((sensor,)))
        elif sensor.get("type") == "sispm":
            tasks.append(sispm_get_data.subtask((sensor,)))
        elif sensor.get("type") == "dummy":
            tasks.append(dummy_get_data.subtask((sensor,)))
        elif sensor.get("type") == "cds":
            tasks.append(cds_get_data.subtask((sensor,)))

    job = group(tasks)

    result = job.apply_async(link=return_real_data.subtask((config, )))

    return 'Started reading real data from sensors %s on device %s at %s' % (config.sensors, config.hostname, time())

@task(name='monitor.return_real_data')
def return_real_data(results, config):

    metering = config.metering
    database = config.database

    for result in results:
        for datum in result:
            metering.send(datum[0], datum[1])
            database.set('%s.%s' % (config.metering_prefix, datum[0]), datum[1])

    return 'Finished reading real data from sensors %s on device %s at %s' % (config.sensors, config.hostname, time())

@task(name='monitor.get_sensor_data.dht')
def dht_get_data(sensor):
    logger.info('Reading sensor: %s' % sensor)
    return get_dht_data(sensor)

@task(name='monitor.get_sensor_data.dummy', track_started=True)
def dummy_get_data(sensor):
    logger.info('Reading sensor: %s' % sensor)
    return get_dummy_data(sensor)

@task(name='monitor.get_sensor_data.sispm', track_started=True)
def sispm_get_data(sensor):
    logger.info('Reading sensor: %s' % sensor)
    return get_sispm_data(sensor)

@task(name='monitor.get_sensor_data.cds', track_started=True)
def cds_get_data(sensor):
    logger.info('Reading sensor: %s' % sensor)
    return get_cds_data(sensor)
