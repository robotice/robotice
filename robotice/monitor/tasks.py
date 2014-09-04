from time import time
import decimal

from celery import group, chord
from celery.task import task
from celery.execute import send_task
from celery.utils.log import get_task_logger

from conf.grains import grains
from utils.functional import import_module

logger = get_task_logger(__name__)


@task(name='monitor.get_real_data')
def get_real_data(config):

    tasks = []
    logger = get_real_data.get_logger()
    logger.info('Sensors {0}'.format(config.sensors))

    for sensor in config.sensors:
        tasks.append(get_sensor_data.subtask(
            (config, sensor, grains), queue='monitor_%s' % config.hostname))
        logger.info('Registred get_sensor_data {0}'.format(sensor))

    job = group(tasks)
    result = job.apply_async()

    return 'Started reading real data from sensors %s on device %s at %s' % (config.sensors, config.hostname, time())


@task(name='monitor.get_sensor_data', track_started=True)
def get_sensor_data(config, sensor, grains):

    LOG = get_real_data.get_logger()

    module_name = ".".join(["monitor", "sensors", sensor.get("device")])

    mod = import_module(module_name)

    results = mod.get_data(sensor)

    LOG.debug("sensor: {0} result: {0}".format(sensor, results))

    for result in results:
        if isinstance(result[1], (int, long, float, decimal.Decimal)):

            result_name = result[0].split('.')[0]
            result_metric = result[0].split('.')[1]

            system, plan_name = config.get_plan(result_name, result_metric)
            
            LOG.debug("for result_name: {0} result_metric: {0} was found".format(
                result_name, 
                result_metric,
                system,
                plan_name))

            if system != None:
                db_key = '%s.%s.%s.%s' % (
                    system.get('name'), 'sensors', plan_name, 'real')
                config.metering.send(db_key, result[1])
                config.database.set(db_key, result[1])

                LOG.debug("metric was sent to database and statsd")

                LOG.debug("metric was sent to database and statsd")

    return 'Started reading real data from sensor %s on device %s at %s' % (sensor, config.hostname, time())
