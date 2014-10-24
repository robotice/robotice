import re

from time import time
import decimal

from datetime import datetime
from celery.task import task
from celery import group, chord
from celery.execute import send_task
from celery.signals import celeryd_after_setup

from robotice.conf import setup_app
from robotice.utils.database import get_db_values
from robotice.reactor.tasks import commit_action

NUMBER = r'(\d+(?:[.,]\d*)?)'

@task(name='reasoner.process_real_data')
def process_real_data(results, sensor):

    LOG = process_real_data.get_logger()

    config = setup_app('reasoner')

    for result in list(results):

        value = result[1]

        if isinstance(value, basestring):
            try:
                value = re.findall(NUMBER, value)[0]
                value = float(value)
            except Exception, e:
                pass

        if isinstance(value, (int, long, float, decimal.Decimal)):

            result_name = result[0].split('.')[0]
            result_metric = result[0].split('.')[1]

            system, plan_name = config.get_plan(result_name, result_metric)
            
            LOG.info("for result_name: {0} result_metric: {1} system: {2} plan: {3}".format(
                result_name, 
                result_metric,
                system,
                plan_name))

            if system != None:
                db_key = '.'.join([
                    system.get('name').replace(".", "_"),
                    plan_name,
                    'real'])
                    
                try:
                    config.metering.send(db_key, value)
                except Exception, e:
                    LOG.error("Fail: send to metering %s " % e)
                
                try:                   
                    redis_status = config.database.set(db_key, value)
                except Exception, er:
                    raise er

                LOG.debug("%s: %s" % (db_key, value))

                LOG.debug("metric was sent to database and statsd")

            else:

                LOG.error("System for device %s and metric %s not found" % (result_name, result_metric))

        else:

            LOG.error("Result from sensor module must be a instance of int, long, float, decimal.Decimal but found %s %s " % (type(value), value))

    return "results: %s" % results


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
        return get_value_for_relay(config, actuator, model_values, real_value)
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

    compared, commits, missing_data = 0, 0, 0

    for actuator in config.actuators:
        # system, plan_name = get_plan(
        #    config, actuator.get('name'), actuator.get("metric"))
        # if not system:
        #    continue
        system = actuator.get('system_name').replace(".", "_")
        key = ".".join([
            actuator.get('system_plan'),
            'sensors',
            actuator.get('plan'),
            ])
        plan_name = config.get(key, config.plans).get("name")
        model_value, real_value = get_db_values(config, system, plan_name)
        logger.info("key: {0} model_value: {1} | real_value: {2}".format(
            ('%s.%s.%s' % (system, 'sensors', plan_name)), model_value, real_value))
        if real_value == None or model_value == None:
            logger.info('NO REAL DATA to COMPARE')
            missing_data += 1
            continue
        actuator_device = config.get_actuator_device(actuator)
        logger.info(actuator_device)
        actuator.update(actuator_device)
        logger.info(actuator)

        if isinstance(model_value, int):

            logger.info("actuator")

            if model_value != real_value:
                logger.info('Registred commit_action for {0}'.format(actuator))
                send_task('reactor.commit_action', args=(
                          config, actuator, model_value, real_value))
                results.append('actuator: {0} hostname: {1}, plan: {2}'.format(
                    actuator.get("name"), actuator.get("name"), plan_name))
        else:

            logger.info("parsed real values : %s < %s and %s < %s" %
                        (model_value[0], real_value, real_value, model_value[1]))
            model_value_converted = get_value_for_actuator(
                config, actuator, model_value, real_value)
            logger.info(
                'converted value for actuator {0}'.format(model_value_converted))

            if (model_value[0] < real_value) \
                and (real_value < model_value[1]):

                model_value_converted = 0
                results.append('OK - actuator: {0} hostname: {1}, plan: {2}'.format(
                    actuator.get("name"), actuator.get("name"), plan_name))
            else:

                logger.info('Registred commit_action for {0}'.format(actuator))

            send_task('reactor.commit_action', args=[
                      config, actuator, str(model_value_converted), str(real_value)])
            results.append('actuator: {0} hostname: {1}, plan: {2}'.format(
                actuator.get("name"), actuator.get("name"), plan_name))

    return results


@celeryd_after_setup.connect
def init_reactors(sender, instance, **kwargs):
    """set default if specified
    """
    config = setup_app('reasoner')

    for name, host in config.devices.iteritems():
        for uuid, actuator in host.get('actuators').iteritems():
            if 'default' in actuator:
                if actuator.get('default') == 'off':
                    model_value = 0
                    real_value = 1
                else:
                    model_value = 1
                    real_value = 0
                send_task('reactor.commit_action', [
                          config, actuator, str(model_value), str(real_value)], {})
