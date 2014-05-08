#!/usr/bin/python

import subprocess
import re
import sys
import logging

logger = logging.getLogger("robotice.sensor.sispm")

def get_data(sensor):
  """
  sispm reading
  """

  if sensor.get('os_family') == 'Debian':
    executable = "/usr/bin/sispmctl"
  else:
    executable = "/usr/local/bin/sispmctl"

  output = subprocess.check_output([executable, "-d", str(sensor.get('port')), "-n", "-m", "all"]);

  lines = output.split("\n")

  data = []
  i = 0
  for line in lines:
    if i != 0:
      status = line.split("\t")
      if len(status) > 1:
        data.append( ["%s.socket%s" % (sensor.get('name'), i), int(status[1])] )
    i += 1
      
  return data
