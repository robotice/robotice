
from time import time
import decimal

from datetime import datetime
from celery.task import task
from celery import group, chord
from celery.execute import send_task
from celery.signals import celeryd_after_setup

from conf import setup_app
from util.database import get_db_values
from util.config import get_plan, get_actuator_device, get_actuators
from reactor.tasks import commit_action

@celeryd_after_setup.connect
def init_reactors(sender, instance, **kwargs):

    config = setup_app('reasoner')

    for host in config.devices:
        for actuator in host.get('actuators'):
            if actuator.has_key('default'):
                if actuator.get('default') == 'off':
                    model_value = 0
                    real_value = 1
                else:
                    model_value = 1
                    real_value = 0
                send_task('reactor.commit_action', [config, actuator, str(model_value), str(real_value)], {})

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


def get_value_for_relay(config, actuator, model_values, real_value):
    if (model_values[0] < real_value) and (real_value < model_values[1]):
        """je v intervalu vse ok"""
        return 0
    if "hum" in actuator.get('plan'):
        if "air" in actuator.get('plan'):
            """zde je potreba odlisit pudni / vzduch kde sou hodnoty naopak"""
            if (real_value < model_values[0]):
                """je mensi jako dolni hranice neni potreba ochlazovat"""
                return 0
            elif (real_value > model_values[1]):
                """je je vetsi jako horni hranice je potreba ochlazovat"""
                return 1
        elif "terra" in actuator.get('plan'):
            """zde je potreba odlisit pudni / vzduch kde sou hodnoty naopak"""
            if (real_value < model_values[0]):
                """je mensi jako dolni hranice je potreba zalevat"""
                return 1
            elif (real_value > model_values[1]):
                """je je vetsi jako horni hranice neni potreba zalevat"""
                return 0
    elif "temp" in actuator.get('plan'):
        if (real_value < model_values[0]):
            """je mensi jako dolni hranice neni potreba ochlazovat"""
            return 0
        elif (real_value > model_values[1]):
            """je je vetsi jako horni hranice je potreba ochlazovat"""
            return 1    
    return 0

def get_value_for_actuator(config, actuator, model_values, real_value):
    """v zavislosti na charakteru actuatoru a planu vrati hodnotu, pokud bude rele zapni vypni 0/1
    pripadne float pro pwm atp
    """
    if "relay" in actuator.get("device"):
        return get_value_for_relay(config,actuator,model_values,real_value)
    else:
        """PWM"""
        return float(0.00)
    return None

@task(name='reasoner.compare_data')
def compare_data(config):
    """
    Core task that runs every 1-60 seconds
    """

    logger = compare_data.get_logger()

    now = time()
    logger.info('Compare data started {0}'.format(now))

    results = []

    actuators = get_actuators(config)

    logger.info(actuators)
    for actuator in actuators:
        #system, plan_name = get_plan(
        #    config, actuator.get('name'), actuator.get("metric"))
        #if not system:
        #    continue
        system = actuator.get('system_name')
        plan_name = actuator.get('plan')
        model_value, real_value = get_db_values(config, system, plan_name)
        logger.info("key: {0} model_value: {1} | real_value: {2}".format(
            ('%s.%s.%s' % (system, 'sensors', plan_name)), model_value, real_value))
        if real_value == None or model_value == None:
            logger.info('NO REAL DATA to COMPARE')
            continue
        actuator_device = get_actuator_device(config, actuator.get('device'))
        actuator.pop('device')
        logger.info(actuator_device)
        actuator.update(actuator_device) 
        logger.info(actuator)
        if isinstance(model_value, int):
            logger.info("actuator")
            if model_value != real_value:
                logger.info('Registred commit_action for {0}'.format(actuator))
                send_task('reactor.commit_action', [config, actuator, model_value, real_value], {})
                results.append('actuator: {0} hostname: {1}, plan: {2}'.format(
                    actuator.get("name"), actuator.get("name"), plan_name))
        else:
            logger.info("parsed real values : %s < %s and %s < %s"% (model_value[0],real_value,real_value, model_value[1]))
            model_value_converted = get_value_for_actuator(config, actuator, model_value, real_value)
            logger.info('converted value for actuator {0}'.format(model_value_converted))
            if (model_value[0] < real_value) and (real_value < model_value[1]):
                model_value_converted = 0
                results.append('OK - actuator: {0} hostname: {1}, plan: {2}'.format(
                    actuator.get("name"), actuator.get("name"), plan_name))
            else:
                logger.info('Registred commit_action for {0}'.format(actuator))
            send_task('reactor.commit_action', [config, actuator, str(model_value_converted), str(real_value)], {})
            results.append('actuator: {0} hostname: {1}, plan: {2}'.format(
                actuator.get("name"), actuator.get("name"), plan_name))

    return results
