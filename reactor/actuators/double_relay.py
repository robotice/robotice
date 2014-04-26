#!/usr/bin/python

import time
import subprocess
import logging

logger = logging.getLogger("robotice")
logger.setLevel(logging.DEBUG)

executable = '/srv/robotice/actuators/relay/driver.py'
interpret = '/srv/robotice/bin/python2'

def run(device, model_data, real_data):

  # python driver.py -a armv7l -p P8_10 -m on

  status_file = '/tmp/robotice_%s' % device.get('name')

  if device.get('reverse', False):
    if model_data == 0:
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'on', '-r','on']
      output1 = subprocess.check_output(command)
      time.sleep(1)
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'off', '-r','on']
      output2 = subprocess.check_output(command)
    else:
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'on', '-r','on']
      output1 = subprocess.check_output(command)
      time.sleep(1)
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'off', '-r','on']
      output2 = subprocess.check_output(command)
  else:
    if model_data == 0:
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'off']
      output1 = subprocess.check_output(command)
      time.sleep(1)
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_1')), '-m', 'on']
      output2 = subprocess.check_output(command)
    else:
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'on']
      output1 = subprocess.check_output(command)
      time.sleep(1)
      command = [interpret, executable, "-a", device.get('architecture'), '-p', str(device.get('port_2')), '-m', 'off']
      output2 = subprocess.check_output(command)


  f = open(status_file, 'w')
  f.write(str(model_data))
  f.close()

  return command, (output1, output2)
