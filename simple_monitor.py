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

# Open a connection to `server` on port `8125` with a `50%` sample rate
statsd_connection = statsd.Connection(
    host='master2.htfs.info',
    port=8125 ,
    sample_rate=0.5,
    disabled = False
)

data = get_dht_data(DUMMY_SENSOR)

print data
 # Create a client for this application
statsd_client = statsd.Client("temp&humidity", statsd_connection)
gauge = statsd.Gauge('MyApplication')

print statsd_client

for datum in data:
  gauge.send(datum[1], datum[2])
