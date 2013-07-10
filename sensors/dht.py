#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime

def get_dht_data(sensor):
  """
  Run the DHT program to get the humidity and temperature readings!
  """
  executable = "/srv/robotice/sensors/Adafruit_DHT"
  version = str(sensor.get('version'))
  port = str(sensor.get('port'))
  output = subprocess.check_output([executable, version, port]);
  print(output)
  matches = re.search("Temp =\s+([0-9.]+)", output)
  if (not matches):
    temp = None
  else:
    temp = float(matches.group(1))
  
  matches = re.search("Hum =\s+([0-9.]+)", output)
  if (not matches):
    humidity = None
  else:
    humidity = float(matches.group(1))

  print("Temperature: %.1f C" % temp)
  print("Humidity:    %.1f %%" % humidity)
 
  values = [
    [datetime.datetime.now(), 'dht.0.temperature', temp],
    [datetime.datetime.now(), 'dht.0.humidity', humidity]
  ]

  return values
