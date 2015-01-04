
import re

import logging
from time import time
from datetime import datetime
from celery.task import task
from celery.execute import send_task
from celery.signals import celeryd_after_setup

from robotice.reactor.tasks import commit_action

from robotice.reasoner.comparators import BaseComparator

logger = logging.getLogger(__name__)

R_FCL_PATH = "/srv/robotice/config/fuzzy"

FCL_VAR = "fcl"

class FuzzyComparator(BaseComparator):
    """Object for handling fuzzy reasoning
    """

    def compare(self):

        for actuator in self.config.actuators:

            system = actuator.get('system_name').replace(".", "_")

            plan_name = actuator["plan_name"]

            fcl_file = actuator.get(FCL_VAR, None)

            if not fcl_file:
                logger.info("Actuator has not specified FCL set, will be ignored.")
                continue

            model_value, real_value = self.get_values(actuator)

            logger.info("key: {0} model_value: {1} | real_value: {2}".format(
                ('%s.%s.%s' % (system, 'sensors', plan_name)), model_value, real_value))
            
            """
            if real_value == None:
                logger.info('NO REAL DATA to COMPARE')
                missing_data += 1
                continue
            """

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
                    "input": real_value,
                }
                output = {
                    "action": 0.0
                }
                
                action = fuzy_system.calculate(inputs, output)["action"]

                logger.info(action)
 
            except Exception, e:
                raise e
            """
            actuator_device = self.config.get_actuator_device(actuator)
            logger.info(actuator_device)
            actuator.update(actuator_device)
            logger.info(actuator)
            """

        return "Fuzzy comparator emit 0 actions."