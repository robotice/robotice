
def get_data(sensor):
  """
  Relay status reading
  """

  status_file = '/tmp/gpio_%s' % sensor.get('port')

  try:
    f = open(status_file, 'r')
    value = int(f.read())
    f.close()
  except:
    value = 0

  data = []
  data.append(("%s.socket" % sensor.get('name'), value))
      
  return data
