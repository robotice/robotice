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
    disabled = False
)
 # Create a client for this application
statsd_client = statsd.Client("temp&humidity", statsd_connection)

class SensorsData():
     #TODO rozdelit v implementaci C
     def getDataFromTemp():
       #prepsat na parametry
       output = subprocess.check_output(["./Adafruit_DHT", "2302", "4"]);
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

       return values = [temp, humidity]

while(True):
  # Run the DHT program to get the humidity and temperature readings!
       def __init__(self):
        # Create a `timer` client
        timer = self.statsd_client.get_client(class_=statsd.Timer)
        # start the measurement
        timer.start()
        gauge = statsd.Gauge('MyApplication')
        # zase rozdelit
        value = SensorsData.getDataFromTemp()
        gauge.send('temperature', value)
        #asi timestamp
        raw.send('temperature', value, datetime.datetime.now())

        timer.interval('10')
        # do something else
        timer.stop('total')
  
  
