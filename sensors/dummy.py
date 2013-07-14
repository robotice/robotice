#!/usr/bin/python

import random
import time
import yaml

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

def get_dummy_data(sensor):
  """
  get dummy data
  """

  timestamp = int(time.time())
  data = []
  data.append( [timestamp, "dummy.data",  random.randint(0, 100)] )
      
  return data
