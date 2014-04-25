
from time import time
import decimal

from datetime import datetime
from celery.task import task
from celery import group, chord
from celery.execute import send_task
from utils import setup_app
from reactor.tasks import commit_action


@task(name='reasoner.process_data')
def process_data(model, data):
    """
    Ships data to some metrics collectors (StatsD)
    save redis as well
    """

    pass


@task(name='reasoner.log_error')
def log_error(model, data):
    """
    Ships data to some metrics collectors (StatsD)
    save redis as well
    """

    pass


@task(name='reasoner.process_real_data')
def process_real_data(results, grains):

    config = setup_app('reasoner')

    metering = config.metering
    database = config.database
    task_results = []

    for datum in results:
        if isinstance(datum[1], (int, long, float, decimal.Decimal)):
            task_results.append(datum)
            metering.send(datum[0], datum[1])

    return 'Finished processing real sensor data %s from device %s at %s' % (task_results, grains.hostname, time())


def get_plan(config, device_name, device_metric):
    """pro dany system vrati plan"""
    for system in config.systems:
        for sensor in system.get('sensors'):
            if device_name == sensor.get('device'):
                return system, sensor.get('plan')
    return None, None


def get_actuator(config, plan_name):
    """pro dany system vrati plan"""
    for system in config.systems:
        for actuator in system.get('actuators'):
            if plan_name == actuator.get('plan'):
                return actuator
    return None


def get_db_values(config, system, plan_name, type='sensors'):
    """return tuple(model_value, real_value)
    """
    try:
        system_name = system.get('name')
    except Exception, e:
        return None, None
    db_key_real = '%s.%s.%s.%s' % (system.get('name'), type, plan_name, 'real')
    db_key_model = '%s.%s.%s.%s' % (
        system.get('name'), type, plan_name, 'model')
    model_value = config.database.get(db_key_model)
    model_value = model_value.replace("(", "").replace(")", "").split(", ")
    if len(model_value) == 1:
        model_value = int(model_value[0])
    else:
        model_value = (int(model_value[0]), int(model_value[1]))
    real_value = config.database.get(db_key_real)
    if real_value:
        real_value = int(real_value)
    return model_value, real_value


@task(name='reasoner.compare_data')
def compare_data(config):
    """
    Core task that runs every 1-60 seconds
    """

    logger = compare_data.get_logger()

    now = time()
    logger.info('Compare data started {0}'.format(now))

    results = []

    logger.info(config.sensors)
    for sensor in config.sensors:
        system, plan_name = get_plan(
            config, sensor.get('name'), sensor.get("metric"))
        if not system:
            continue
        model_value, real_value = get_db_values(config, system, plan_name)
        logger.info("key: {0} model_value: {1} | real_value: {2}".format(
            ('%s.%s.%s' % (system.get('name'), 'sensors', plan_name)), model_value, real_value))
        if not real_value:
            logger.info('NO REAL DATA to COMPARE')
            continue
        actuator = sensor
        actuator_ = get_actuator(config, plan_name)
        if actuator_:
            actuator["extra"] = actuator_.pop("device")
            logger.info(actuator)
        else:
            logger.info("missing actuator %s"% sensor)
        if isinstance(model_value, int):
            logger.info("actuator")
            if model_value != real_value:
                logger.info('Registred commit_action for {0}'.format(sensor))
                send_task('reactor.commit_action', [config, actuator, model_value, real_value], {})
                results.append('sensor: {0} hostname: {1}, plan: {2}'.format(
                    sensor.get("name"), sensor.get("hostname"), plan_name))
        else:
            logger.info("parsed real values : %s < %s and %s < %s"% (model_value[0],real_value,real_value, model_value[1]))
            if (model_value[0] < real_value) and (real_value < model_value[1]):
                results.append('OK - sensor: {0} hostname: {1}, plan: {2}'.format(
                    sensor.get("name"), sensor.get("hostname"), plan_name))
            else:
                logger.info('Registred commit_action for {0}'.format(sensor))
                send_task('reactor.commit_action', [config, actuator, model_value, real_value], {})
                results.append('sensor: {0} hostname: {1}, plan: {2}'.format(
                    sensor.get("name"), sensor.get("hostname"), plan_name))

    return results
