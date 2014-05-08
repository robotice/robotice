#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

python = '/srv/robotice/bin/python2'
executable = '/srv/robotice/actuators/relay/driver.py'

def run(device, model_data, real_data):

  # python driver.py -a armv7l -p P8_10 -m on

  if device.get('reverse', False):

    if int(model_data) == 0:
      command = [python, executable, '-p', str(device.get('port')), '-m', 'off', '-r', 'on']
    else:
      command = [python, executable, '-p', str(device.get('port')), '-m', 'on', '-r', 'on']

  else:

    if int(model_data) == 0:
      command = [python, executable, '-p', str(device.get('port')), '-m', 'off']
    else:
      command = [python, executable, '-p', str(device.get('port')), '-m', 'on']

  output = subprocess.check_output(command)
  
  return command, output