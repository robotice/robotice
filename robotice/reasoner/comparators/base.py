import re
import logging
import decimal
import pickle
from datetime import datetime
from celery.task import task
from celery import group, chord
from celery.execute import send_task
from celery.signals import celeryd_after_setup

from robotice.conf import setup_app
from robotice.utils.database import get_db_values
from robotice.reactor.tasks import commit_action

logger = logging.getLogger(__name__)

# TODO: move to utils
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

class BaseComparator(object):
    """Object for handling simple reasoning

    :param:config: Robotice settings
    """

    def compare(self):

        compared, actions, missing_data = 0, 0, 0

        for actuator in self.config.actuators:

            system = actuator.get('system_name')
            plan_name = actuator["plan_name"]

            model_value, real_value = self.get_values(actuator)

            recurence_db_key = ':'.join([str(system), str(plan_name), 'recurrence'])

            logger.info("key: {0} model_value: {1} | real_value: {2}".format(
                ('%s:%s:%s' % (system, 'sensors', plan_name)), model_value, real_value))
            if real_value == None or model_value == None:
                logger.info('NO REAL DATA to COMPARE')
                self.config.db.incr(recurence_db_key)
                missing_data += 1
                continue
            actuator_device = self.config.get_actuator_device(actuator)
            logger.info(actuator_device)
            actuator.update(actuator_device)
            logger.info(actuator)

            if isinstance(model_value, int):

                logger.info("actuator")

                if model_value != real_value:
                    logger.info('Registred commit_action for {0}'.format(actuator))
                    send_task('reactor.commit_action', args=(
                              actuator, model_value, real_value, self.config))
                    actions += 1
                    logger.info('actuator: {0} model_value: {1} real_value: {2}'.format(
                        actuator.get("name"), model_value, real_value))
                    # increment recurrence
                    self.config.db.incr(recurence_db_key)
                else:
                    self.config.db.set(recurence_db_key, 0)
            else:

                logger.info("parsed real values : %s < %s and %s < %s" %
                            (model_value[0], real_value, real_value, model_value[1]))
                model_value_converted = get_value_for_actuator(
                    self.config, actuator, model_value, real_value)
                logger.info(
                    'converted value for actuator {0}'.format(model_value_converted))

                if (model_value[0] < real_value) \
                    and (real_value < model_value[1]):

                    model_value_converted = 0
                    logger.info('OK - actuator: {0} hostname: {1}, plan: {2}'.format(
                        actuator.get("name"), actuator.get("name"), plan_name))
                else:

                    logger.info('Registred commit_action for {0}'.format(actuator))

                send_task('reactor.commit_action', args=[
                          actuator, str(model_value_converted), str(real_value), self.config])
                actions += 1
                logger.info('actuator: {0} hostname: {1}, plan: {2}'.format(
                    actuator.get("name"), actuator.get("name"), plan_name))

        return "Simple comparator emit {0} actions.".format(actions)

    def get_values(self, actuator):

        system = actuator.get('system_name')

        plan_name = actuator["plan_name"]
        return get_db_values(self.config, system, plan_name)
    
    def __init__(self, config):

        super(BaseComparator, self).__init__()
        self.config = config