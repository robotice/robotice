#!/usr/bin/python

import random

def get_data(sensor):
  """
  relay reading
  """
  output = ""
   
  lines = output.split("\n")
  data = []
  i = 0
  for line in lines:
    if i != 0:
      status = line.split("\t")
      if len(status) > 1:
        data.append( ["relay1.socket_%s" % i, int(status[1])] )
    i += 1
      
  return data
