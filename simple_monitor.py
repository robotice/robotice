#!/usr/bin/python

import subprocess
import re
import sys
import time
import datetime
import statsd
import yaml
import undead

from sensors.dht import get_dht_data
from sensors.sis_pm import get_sispm_data

config_file = open("/srv/robotice/config.yml", "r")

config = yaml.load(config_file)

#damon setting
undead.name = "simple-monitor-daemon"
undead.process_name = "monitordaemon"

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

def send_data(data):
	if data != None:
		for datum in data:
			print datum
			gauge.send(datum[1], datum[2])

@undead
def deamon_test():
	while True:
		for sensor in config.get("sensors"):
			if sensor.get("type") == "dht":
				data = get_dht_data(sensor)
  				send_data(data)
  			elif sensor.get("type") == "sispm":
				data = get_sispm_data()
				send_data(data)
  			
		time.sleep(2)
