
from time import time
import decimal

from datetime import datetime 
from celery.task import task

from utils import setup_app

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
            if sensor.get('device') == device_name and sensor.get('metric') == device_metric:
                return system, sensor.get('plan')
    return None, None

def get_db_values(config, system, plan_name, type='sensor'):
    """return tuple(model_value, real_value)
    """
    db_key_real = '%s.%s.%s.%s' % (system, type, plan_name, 'real')
    db_key_model = '%s.%s.%s.%s' % (system, type, plan_name, 'model')
    model_value = config.database.get(db_key_model)
    real_value = config.database.get(db_key_real)
    return (model_value, real_value)

@task(name='reasoner.compare_data')
def compare_data(config):
    """
    Core task that runs every 1-60 seconds
    """

    logger = compare_data.get_logger()
    
    now = time()    
    logger.info('Compare data started {0}'.format(now))

    results = []
    tasks = []

    for system in config.systems:
        for sensor in config.sensors:
            system, metric = config.get_system_for_device(sensor.get("name")) #dht1")
            system, plan_name = get_plan(config, sensor.get('name'), metric)
            model_value, real_value = get_db_values(config, system, plan_name)
            results.append((model_value, real_value),)
            if model_value == real_value:
                tasks.append(commit_action.subtask((config, sensor, grains), exchange='reactor_%s' % config.hostname))
                logger.info('Registred commit_action {0}'.format(sensor))
    
    job = group(tasks)
    result = job.apply_async()
    
    return result
