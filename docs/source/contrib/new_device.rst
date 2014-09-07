=================
Add support for new device
=================

Sensor
=========

For every sensor which was found in `devices.yml` Robotice looking for python module in `monitor/sensors/<sensor_type>.py`. Each module has method **get_data** with one argument *dict* sensor

.. code-block:: python

	#!/usr/bin/python

	import subprocess
	import re
	import sys
	import logging

	logger = logging.getLogger("robotice.sensor.sispm")

	def get_data(sensor):
	  """
	  sispm reading
	  """

	  # adapt for specific OS internals

	  if sensor.get('os_family') == 'Debian':
	    executable = "/usr/bin/sispmctl"
	  else:
	    executable = "/usr/local/bin/sispmctl"

	  # call executable 

	  output = subprocess.check_output([executable, "-d", str(sensor.get('port')), "-n", "-m", "all"]);

	  # parse output

	  lines = output.split("\n")

	  data = []
	  i = 0
	  for line in lines:
	    if i != 0:
	      status = line.split("\t")
	      if len(status) > 1:
	        data.append( ["%s.socket%s" % (sensor.get('name'), i), int(status[1])] )
	    i += 1
	  
	  # return data
	  # return list of tuples [(metric.name, value)]

	  return data

Actuator
========

For every sensor which was found in `devices.yml` Robotice looking for python module in `monitor/sensors/<sensor_type>.py`. Each module has method **run** with accepts three arguments *dict* device, model_data and real data is values which may take few data types boolean or 0 / 1, maybe float with number percent level 0.75 or something more complex. 

Sispm as actuator
-----

.. code-block:: python

	#!/usr/bin/python

	import time
	import subprocess
	import logging

	logger = logging.getLogger("robotice")
	logger.setLevel(logging.DEBUG)

	def run(device, model_data, real_data):

	  if device.get('os_family') == 'Arch':
	    executable = "/usr/local/bin/sispmctl"
	  else:
	    executable = "/usr/bin/sispmctl"

	  if int(model_data) == 0:
	    command = [executable, "-d", str(device.get('port')), '-f', str(device.get('socket'))]
	  else:
	    command = [executable, "-d", str(device.get('port')), '-o', str(device.get('socket'))]

	  output = subprocess.check_output(command);

	  return command, output