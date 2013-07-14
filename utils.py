#!/usr/bin/python

import logging

from sensors.dht import get_dht_data
from sensors.sis_pm import get_sispm_data
from sensors.dummy import get_dummy_data

log = logging.getLogger("robotice.monitor")

def send_data(config, data, sender):
	if data != None:
		for datum in data:
			#log.info(datum)
			sender.send(datum[1], datum[2])

def collect_data(config, sender):
	for sensor in config.get("sensors"):
		if sensor.get("type") == "dht":
			data = get_dht_data(sensor)
			send_data(config, data, sender)
			#log.info("dht:%s:%s" % (sensor.get("port"), data))
		elif sensor.get("type") == "sispm":
			data = get_sispm_data(sensor)
			send_data(config, data, sender)  			
			#log.info("sispm:%s:%s" % (sensor.get("device"), data))
		elif sensor.get("type") == "dummy":
			data = get_dummy_data(sensor)
			send_data(config, data, sender)  			
			#log.info("dummy:%s:%s" % (sensor.get("device"), data))
		else:
			log.info("unhandled device")