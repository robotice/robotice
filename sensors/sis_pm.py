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
  output = subprocess.check_output([executable, "-m", "all"]);

  if config.get("debug"):
    print output

  return output
