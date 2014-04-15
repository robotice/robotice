from time import time
import decimal

from celery import group, chord
from celery.task import task
from celery.execute import send_task
from celery.utils.log import get_task_logger

from reasoner.tasks import process_real_data, log_error

from utils import get_grains

logger = get_task_logger(__name__)

@task(name='monitor.get_real_data')
def get_real_data(config):

    tasks = []
    logger = get_real_data.get_logger()
    #grains = get_grains()
    logger.info('Sensors {0}'.format(config.sensors))
    
    for sensor in config.sensors:
        tasks.append(get_sensor_data.subtask((sensor,), exchange='monitor_%s' % config.hostname))
        logger.info('Registred get_sensor_data {0}'.format(sensor))

    job = group(tasks)
    result = job.apply_async(link=process_real_data.subtask((config, ), exchange='reasoner'))
    return result #'Started reading real data from sensors %s on device %s at %s' % (config.sensors, config.hostname, time())

def import_module(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

@task(name='monitor.get_sensor_data', track_started=True)
def get_sensor_data(sensor):

    module_name = ".".join(["monitor", "sensors", sensor.get("device")])

    mod = import_module(module_name)
    return mod.get_data(sensor)
