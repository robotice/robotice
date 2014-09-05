from time import time
import decimal

from celery import group, chord
from celery.task import task
from celery.execute import send_task
from celery.utils.log import get_task_logger

from conf.grains import grains
from conf import setup_app
from utils.functional import import_module

logger = get_task_logger(__name__)


@task(name='monitor.get_real_data')
def get_real_data(config):

    tasks = []
    logger = get_real_data.get_logger()
    logger.info('Sensors {0}'.format(config.sensors))

    for sensor in config.sensors:
        tasks.append(get_sensor_data.subtask(
            (config, sensor, grains), exchange='monitor_%s' % config.hostname))
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
            
            LOG.info("for result_name: {0} result_metric: {1} system: {2} plan: {3}".format(
                result_name, 
                result_metric,
                system,
                plan_name))

            if system != None:
                db_key = '.'.join([system.get('name'), 'sensors', sensor.get("name"), 'real'])
                    
                config = setup_app("monitor")
                
                try:
                    config.metering.send(db_key, result[1])
                except Exception, e:
                    LOG.error("Fail: send to metering %s " % e)
                
                try:                   
                    redis_status = config.database.set(db_key, result[1])
                except Exception, er:
                    raise er

                LOG.debug("%s: %s" % (db_key, result[1]))

                LOG.debug("metric was sent to database and statsd")

            else:

                LOG.error("System for device %s not found" % result_name)

        else:

            LOG.error("Result from sensor module must be a instance of int, long, float, decimal.Decimal but found %s %s " % (type(result[1]), result[1]))

    return 'Started reading real data from sensor %s on device %s at %s' % (sensor, config.hostname, time())
