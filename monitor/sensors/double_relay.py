#!/usr/bin/python

def get_data(sensor):
  """
  relay reading
  """
  value = 0
  
  data = []
  data.append(("%s.socket" % sensor.get('name'), value))
      
  return data
