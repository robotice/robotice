#!/usr/bin/python
import subprocess
import re
import sys
import time
import yaml

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)
executable = "/usr/local/bin/sispmctl"

def get_sispm_data():
  """
  sispm
  """
  return subprocess.check_output([executable, "-m", "all"]);

def get_sispm_data_from_sensor(socket):
  """
  get data from one sensor
  """
  return subprocess.check_output([executable, "-m", socket]);
