#!/usr/bin/python

import subprocess
import re
import sys
import statsd
import yaml
import undead

from time import sleep
from simple_monitor import send_data_all

undead.name = "robotice-daemon"
undead.proc_title = "robotice"
undead.settings["pidfile"] = "/tmp/robotice.pid"

@undead
def robotice(log):
	log.info("start initial config")
	config_file = open("/srv/robotice/config.yml", "r")
	config = yaml.load(config_file)

	#add additional settings
	statsd_connection = statsd.Connection(
	    host=config.get("statsd").get("host"),
	    port=config.get("statsd").get("port"),
	    sample_rate=1,
	    disabled = False
	)
	log.info("statsd config %s" %statsd_connection)
	# Create a client for this application
	#statsd_client = statsd.Client("temp&humidity", statsd_connection)
	sender = statsd.Gauge('robotice_prod.%s' %config.get("name").replace(".","_"), statsd_connection)
	#log.info("daemon: %s \n pidfile: %s" %undead.proc_title %undead.settings["pidfile"])
	while True:
		send_data_all(log,config,sender)
		sleep(2)

