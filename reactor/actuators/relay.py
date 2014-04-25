#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

executable = '/srv/robotice/actuators/relay/driver.py'

def run_action(device, model_data, real_data):

  # python driver.py -a armv7l -p P8_10 -m on

  if model_data == 0:
    command = ['python', executable, "-a", device.get('architecture'), '-p', device.get('port'), '-m', 'off']
  else:
    command = ['python', executable, "-a", device.get('architecture'), '-p', device.get('port'), '-m', 'on']

  output = subprocess.check_output(command);

  return output
