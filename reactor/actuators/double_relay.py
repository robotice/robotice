#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

executable = '/srv/robotice/bin/poython /srv/robotice/actuators/relay/driver.py'

def run(device, model_data, real_data):

  # python driver.py -a armv7l -p P8_10 -m on

  status_file = '/tmp/robotice_%s' % device.get('name')

  if device.get('reverse', False):
    if model_data == 0:
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'on', '-r','on']
      time.sleep(1)
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'off', '-r','on']
    else:
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'on', '-r','on']
      time.sleep(1)
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'off', '-r','on']
  else:
    if model_data == 0:
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'off']
      time.sleep(1)
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'on']
    else:
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'on']
      time.sleep(1)
      command = [executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'off']

  output = subprocess.check_output(command)

  f = open(status_file, 'w')
  f.write(str(model_data))
  f.close()

  return command, output
