
import re

import logging
from time import time
from datetime import datetime
from celery.task import task
from celery.execute import send_task
from celery.signals import celeryd_after_setup
import random
from robotice.reactor.tasks import commit_action

from robotice.reasoner.comparators import BaseComparator

logger = logging.getLogger(__name__)

R_FCL_PATH = "/srv/robotice/config/fuzzy"

FCL_VAR = "fcl"

class FuzzyComparator(BaseComparator):
    """Object for handling fuzzy reasoning
    
    this comparator use pyfuzzy library witch depends on antlr

    http://sourceforge.net/projects/pyfuzzy
    https://pypi.python.org/pypi/antlr_python_runtime/3.1.2

    export PYTHONPATH:$PYTHONPATH:/srv/robotice/lib/python2.7/site-packages/fuzzy

    and add fuzzy comparator into reasoner.ini pipeline

    """

    def compare(self):

        actions = 0

        for actuator in self.config.actuators:

            system = actuator.get('system_name')

            plan_name = actuator["plan_name"]

            fcl_file = plan_name # todo actuator["plan_full"] and get cycles fcl #actuator.get(FCL_VAR, None)

            if not fcl_file:
                logger.info("Actuator has not specified FCL set, will be ignored.")
                continue

            model_value, real_value = self.get_values(actuator)

            logger.info("key: {0} model_value: {1} | real_value: {2}".format(
                ('%s.%s.%s' % (system, 'sensors', plan_name)), model_value, real_value))
            
            if not real_value:
                #logger.warning("no real data for fuzzy compare, real_value was randomly generated")
                real_value = random.uniform(0, 100)

            # try load pyfuzzy
            try:
                import fuzzy.storage.fcl.Reader
            except Exception, e:
                logger.error("Missing pyfuzzy library. Maybe pip install pyfuzzy fix this issue. Original exception: {0}".format(e))
                raise e # cannot continue


            # load FCL file
            fcl_file = ".".join([fcl_file, "fcl"])
            fcl_path = "/".join([R_FCL_PATH, fcl_file])
            try:
                fuzy_system = fuzzy.storage.fcl.Reader.Reader().load_from_file(fcl_path)
            except Exception, e:
                logger.warning("Cannot load FCL file {0} in {1} path.".format(fcl_file, fcl_path))

            # process FCL and get action
            logger.info("Ready to FCL calculate")
            
            try:
                inputs = {
                    "real_value": real_value,
                }
                output = {
                    "action": 0.0
                }
                
                action = fuzy_system.calculate(inputs, output)["action"]

                actuator_device = self.config.get_actuator_device(actuator)
                actuator.update(actuator_device)

                logger.info("Fuzzy computed %s for value %s actuator: %s" % (action, real_value, actuator))
 
                send_task('reactor.commit_action', args=[
                          actuator, action, real_value, self.config])

                actions += 1

            except Exception, e:
                raise e

        return "Fuzzy comparator emit %s actions." % actions