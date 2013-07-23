#!/usr/bin/python

import random

def get_dummy_data(sensor):
  """
  get dummy data
  """

  data = []
  data.append( ["dummy.0.data",  random.randint(0, 100)] )
      
  return data
