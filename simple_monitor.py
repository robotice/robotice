#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import statsd
import yaml
import RPi.GPIO as GPIO

from sensors.dht import get_dht_data
from sensors.sis_pm import get_sispm_data

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

if config.get("debug"):
	print config

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
	for sensor in config.get("sensors"):
		if sensor.get("type") == "dht":
			data = get_dht_data(sensor)
  			gauge.send(data[1], data[2])
	get_sispm_data()
	if data == None:
		break
	GPIO.setup(24, GPIO.OUT)
	GPIO.output(24, False)
	time.sleep(2)
	GPIO.output(24, True)