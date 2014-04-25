from time import time
import decimal

from celery import group, chord
from celery.task import task
from celery.execute import send_task
from celery.utils.log import get_task_logger

from reasoner.tasks import process_real_data, log_error

from utils import get_grains, import_module

logger = get_task_logger(__name__)

def get_plan(config, device_name, device_metric):
    """pro dany system vrati plan"""
    for system in config.systems:
        for sensor in system.get('sensors'):
            if sensor.get('device') == device_name and sensor.get('metric') == device_metric:
                return system, sensor.get('plan')
    return None, None

@task(name='monitor.get_real_data')
def get_real_data(config):

    tasks = []
    logger = get_real_data.get_logger()
    grains = get_grains()
    logger.info('Sensors {0}'.format(config.sensors))
    
    for sensor in config.sensors:
        tasks.append(get_sensor_data.subtask((config, sensor, grains), exchange='monitor_%s' % config.hostname))
        logger.info('Registred get_sensor_data {0}'.format(sensor))

    job = group(tasks)
    result = job.apply_async()

    return 'Started reading real data from sensors %s on device %s at %s' % (config.sensors, config.hostname, time())

@task(name='monitor.get_sensor_data', track_started=True)
def get_sensor_data(config, sensor, grains):

    module_name = ".".join(["monitor", "sensors", sensor.get("device")])

    mod = import_module(module_name)

    results = mod.get_data(sensor)

    for result in results:
        if isinstance(result[1], (int, long, float, decimal.Decimal)):
            

            result_name = result[0].split('.')[0]
            result_metric = result[0].split('.')[1]

            system, plan_name = get_plan(config, result_name, result_metric)
            if system != None:
                db_key = '%s.%s.%s.%s' % (system.get('name'), 'sensors', plan_name, 'real')    
                config.metering.send(db_key, result[1])
                config.database.set(db_key, result[1])
            
            #return result[0].split('.')[-1]
    return results

#@task(name='monitor.return_sensor_data', track_started=True)
#def return_sensor_data(results, config):

#    send_task("reasoner.process_real_data",[results, config], {})

#    return results
