#!/usr/bin/python
import subprocess
import re
import sys
import time
import yaml

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

def get_sispm_data():
  """
  sispcml
  """
  executable = "/usr/local/bin/sispmctl"
  values = []
  for socket in xrange(1,4):
    output = subprocess.check_output([executable, "-m", socket]);
    values[socket] = [timestamp = int(time.time()),"sispm.0.{socket}", output]
    if config.get("debug"):
      print values[socket]

  return values
