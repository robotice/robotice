#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import python-statsd

# Open a connection to `server` on port `8125` with a `50%` sample rate
statsd_connection = statsd.Connection(
    host='server',
    port=8125 ,
    sample_rate=0.5,
)
 # Create a client for this application
statsd_client = statsd.Client("temp&humidity", statsd_connection)

class Monitor(object):
     def __init__(self):
        # Create a client specific for this class
        self.statsd_client = statsd_client.get_client(
        self.__class__.__name__)

     def do_something(self):
        # Create a `timer` client
        timer = self.statsd_client.get_client(class_=statsd.Timer)
        # start the measurement
        timer.start()
        # do something
        timer.interval('intermediate_value')
        # do something else
        timer.stop('total')

# Continuously append data
while(True):
  # Run the DHT program to get the humidity and temperature readings!
  output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);
  print output
  matches = re.search("Temp =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  temp = float(matches.group(1))
  
  # search for humidity printout
  matches = re.search("Hum =\s+([0-9.]+)", output)
  if (not matches):
	time.sleep(3)
	continue
  humidity = float(matches.group(1))

  print "Temperature: %.1f C" % temp
  print "Humidity:    %.1f %%" % humidity

  values = [datetime.datetime.now(), temp, humidity]
