#!/usr/bin/python

import random

def get_dummy_data(sensor):
  """
  get dummy data
  """

  data = []
  data.append( ["dummy.%s.data_1" % sensor.get('device'),  random.randint(0, 100)] )
  data.append( ["dummy.%s.data_2" % sensor.get('device'),  random.randint(0, 100)] )
      
  return data
