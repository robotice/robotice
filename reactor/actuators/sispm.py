#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

executable = "/usr/local/bin/sispmctl"

def run(device, model_data, real_data):

  if model_data == 0:
    command = [executable, "-d", str(device.get('device')), '-f', str(device.get('system').get('socket'))]
  else:
    command = [executable, "-d", str(device.get('device')), '-o', str(device.get('system').get('socket'))]

  output = subprocess.check_output(command);

  return output
