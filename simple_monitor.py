#!/usr/bin/python

from sensors.dht import get_dht_data
from sensors.sis_pm import get_sispm_data

def send_data(data,sender):
	if data != None:
		for datum in data:
			print datum
			sender.send(datum[1], datum[2])

def send_data_all(log, config,sender):
	for sensor in config.get("sensors"):
		if sensor.get("type") == "dht":
			data = get_dht_data(sensor)
			send_data(data,sender)
			log.info("dht:%s %s"%sensor.get("port") %data)
		elif sensor.get("type") == "sispm":
			data = get_sispm_data()
			send_data(data,sender)  			
			log.info("sispm:%s %s"%sensor.get("port") %data)