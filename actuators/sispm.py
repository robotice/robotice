#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

executable = "/usr/local/bin/sispmctl"

def run_action(device, delay):

  on_command = [executable, "-d", str(device.get('device')), '-o', str(device.get('socket'))]
  off_command = [executable, "-d", str(device.get('device')), '-f', str(device.get('socket'))]

  try:
    output = subprocess.check_output(on_command);
  except Exception, e:
    print e
    return None

  time.sleep(delay)

  try:
    output = subprocess.check_output(off_command);
  except Exception, e:
    print e
    return None
