#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

executable = "/usr/local/bin/sispmctl"

def run_action(device, model_data, real_data):

  if model_data == 0:
    command = [executable, "-d", str(device.get('device')), '-f', str(device.get('socket'))]
  else:
    command = [executable, "-d", str(device.get('device')), '-o', str(device.get('socket'))]

  output = subprocess.check_output(command);

  return output
