#!/usr/bin/python

import random
import yaml

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

def get_dummy_data(sensor):
  """
  get dummy data
  """

  data = []
  data.append( ["dummy.0.data",  random.randint(0, 100)] )
      
  return data
