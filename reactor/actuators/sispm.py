#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

def run(device, model_data, real_data):

  if device.get('os_family') == 'Debian':
    executable = "/usr/bin/sispmctl"
  else:
    executable = "/usr/local/bin/sispmctl"


  if int(model_data) == 0:
    command = [executable, "-d", str(device.get('port')), '-f', str(device.get('socket'))]
  else:
    command = [executable, "-d", str(device.get('port')), '-o', str(device.get('socket'))]

  output = subprocess.check_output(command);

  return command, output