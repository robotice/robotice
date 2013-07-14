#!/usr/bin/python
import subprocess
import re
import sys
import time
import yaml

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)
executable = "/usr/local/bin/sispmctl"

def get_sispm_data(sensor):
  """
  sispm
  """
  try:
    output = subprocess.check_output([executable,"-d", "0" ,"-n" ,"-m", "all"]);
  except Exception, e:
    return None

  lines = output.split("\n")
  timestamp = int(time.time())
  data = []
  i = 0
  for line in lines:
    if i != 0:
      status = line.split("\t")
      if len(status) > 1:
        data.append( [timestamp, "sismp.0.socket_%s" % i, int(status[1])] )
    i += 1
      
  return data

def get_sispm_data_from_sensor(socket):
  """
  get data from one sensor
  """
  return subprocess.check_output([executable, "-m", socket]);
