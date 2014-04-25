
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


@task(name='reasoner.compare_data')
def compare_data(config):
    """
    Core task that runs every 1-60 seconds
    """

    now = time()

    for system in config.systems:
        system, metric config.get_system_for_device(system.get('sensors')[0].get('device'))
    
    return 0
