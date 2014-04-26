#!/usr/bin/python

def get_data(sensor):
  """
  relay reading
  """
  value = 0
  
  status_file = '/tmp/robotice_%s' % sensor.get('name')

  try:
    f = open(status_file, 'w')
    value = int(f.read())
    f.close()
  except:
    pass

  data = []
  data.append(("%s.socket" % sensor.get('name'), value))
      
  return data
