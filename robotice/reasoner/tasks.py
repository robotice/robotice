import re

from time import time
import decimal
import pickle
import datetime
from celery.task import task
from celery import group, chord
from celery.execute import send_task
from celery.signals import celeryd_after_setup

from robotice.conf import setup_app
from robotice.utils.database import get_db_values
from robotice.reactor.tasks import commit_action

from kombu.utils import symbol_by_name

NUMBER = r'(\d+(?:[.,]\d*)?)'

NO_DATA_TO_COMPARE_FMT = """
    for {system} {actuator} {plan} has not data
"""

@task(name='reasoner.process_real_data')
def process_real_data(results, sensor):

    LOG = process_real_data.get_logger()

    config = setup_app('reasoner')

    processed = 0
    db_saved = 0

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

            system, plan = config.get_plan(result_name, result_metric)
            """
            key = ".".join([
                "*",
                "*",
                result_name,
                "device"
                ])
            
            keys = config.database.keys(key)
            for _key in keys:
                device = config.database.hgetall(_key)
            
            device = config.database.hgetall(key)
            if not device:
                raise Exception("%s not found in db" % key)
            """

            if not plan:
                LOG.error("Missing plan for result %s and metric %s, value %s will be ignored. See log for more detail." % (result_name, result_metric, value))
                continue

            if system != None:
                db_key = ':'.join([
                    str(system["name"]),
                    str(plan["name"]),
                    'real'])
                    
                try:
                    config.metering.send(db_key, value)
                    processed += 1
                except Exception, e:
                    LOG.error("Fail: send to metering %s " % e)
                
                try:                   
                    redis_status = config.database.set(db_key, value)
                    db_saved += 1
                except Exception, er:
                    raise er

                LOG.debug("%s: %s" % (db_key, value))

            else:

                LOG.error("System for device %s and metric %s not found and was skipped." % (result_name, result_metric))

        else:

            LOG.error("Result from sensor module must be a instance of int, long, float, decimal.Decimal but found %s %s and was ignored." % (type(value), value))

    return "total: %s : sent to graphite: %s saved to db: %s" % (len(results), processed, db_saved)

@task(name='reasoner.compare_data')
def compare_data(config):
    """
    Core task that runs every 1-60 seconds
    """

    logger = compare_data.get_logger()

    now = time()

    logger.info('Compare data started {0}'.format(now))

    results = []

    for alias, comparator_path in config.comparators.iteritems():
        
        # inicialize comparator
        try:
            comparator_cls = symbol_by_name(comparator_path)
            comparator = comparator_cls(config)
        except Exception, e:
            logger.warning('Initialize comparator {0} was failed {1}, next processing will be skipped.'.format(comparator_path, e))

        if comparator:
            # process compare
            try:
                compare_results = comparator.compare()
                results.append(compare_results)
                logger.info("Results {0} from {1} comparator".format(compare_results, alias))
            except Exception, e:
                logger.error('Process comparator({0}) compare was failed {1}'.format(comparator_path, e))

    logger.info('Compared completed in {0}s'.format(time() - now))

    return results


@celeryd_after_setup.connect
def init_reactors(sender, instance, **kwargs):
    """set default if specified
    """
    config = setup_app('reasoner')

    for name, host in config.devices.list().iteritems():
        for uuid, actuator in host.get('actuators').iteritems():
            if 'default' in actuator:
                if actuator.get('default') == 'off':
                    model_value = 0
                    real_value = 1
                else:
                    model_value = 1
                    real_value = 0
                send_task('reactor.commit_action', [
                          actuator, str(model_value), str(real_value), config], {})
