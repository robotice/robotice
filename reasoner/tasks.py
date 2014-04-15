
from time import time
import decimal

from datetime import datetime 
from celery.task import task

#from planner.tasks import get_model_data
#from reactor.tasks import commit_action

@task(name='reasoner.compare_data')
def compare_data(model, real_data, model_data):
    """
    Compares model and real data and returns list of actions to do
    """

    return []

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
def process_real_data(results, config):

    metering = config.metering
    database = config.database
    task_results = []

#    for result in results.join():
    for datum in results:
        if isinstance(datum[1], (int, long, float, decimal.Decimal)):
            task_results.append(datum)
            metering.send(datum[0], datum[1])

    return 'Finished reading real data %s on device %s at %s' % (task_results, config.hostname, time())


@task(name='reasoner.maintain_system')
def maintain_system(config):
    """
    Core task that runs every 1-60 seconds
    """

    now = time()

    # Ask planner for system shape - all sensors, actuators
#    model = get_model.delay().get()

    # send model data ranges upstream
#    log_data(model_data)

    # Depending on model get real data from all sensors
#    real_data, metering_log = get_real_data.delay(model).get()

    # send real collected metrics upstream
#    log_data(real_data)

    # send data collection statistics (reading retries)
#    log_data(metering_log)

    # Compare real data with model data and get list of actions to do

    compare_data.apply_async(args=[None, None], queue='reasoner', routing_key='reasoner.compare_data')

 #   action_results = []

 #   for action in model.get('sensors'):
        # Commit each action and return status code
 #       action_results.append(commit_action.delay(action).get())

    # send action performance statistics
 #   log_data(action_results)

    return 0
