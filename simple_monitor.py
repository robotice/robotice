#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import statsd

from sensors.dht import get_dht_data

DUMMY_SENSOR = {
    'version': 2302,
    'port': 4
}
DUMMY_SENSOR1 = {
    'version': 11,
    'port': 18
}

# Open a connection to `server` on port `8125` with a `50%` sample rate
statsd_connection = statsd.Connection(
    host='master2.htfs.info',
    port=8125 ,
    sample_rate=0.5,
    disabled = False
)

# Create a client for this application
statsd_client = statsd.Client("temp&humidity", statsd_connection)
gauge = statsd.Gauge('MyApplication', statsd_connection)
raw = statsd.Raw('MyApplication', statsd_connection)

print ("statsd client: ",statsd_client)

while True:
	data = get_dht_data(DUMMY_SENSOR)
	data1 = get_dht_data(DUMMY_SENSOR1)
	if (data == null and data1 == null)
		break
	print ("data is ",data)
	for datum in data:
  		gauge.send(datum[1], datum[2])
  	for datum1 in data1
  		gauge.send(datum1[1], datum1[2])
  		#raw.send('SomeName', value, datetime.datetime.now())
	time.sleep(2)