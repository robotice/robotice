#!/usr/bin/python

import subprocess
import re
import sys
import logging

executable = "/usr/local/bin/sispmctl"
logger = logging.getLogger("robotice.sensor.afm")

def get_data(sensor):
  """
  sispm reading
  """
  try:
    output = subprocess.check_output([executable,"-d", "0" ,"-n" ,"-m", "all"]);
  except Exception, e:
    logger.info('Call to socket failed')
    return None

  lines = output.split("\n")
  data = []
  i = 0
  for line in lines:
    if i != 0:
      status = line.split("\t")
      if len(status) > 1:
        data.append( ["sismp.0.socket_%s" % i, int(status[1])] )
    i += 1
      
  return data
