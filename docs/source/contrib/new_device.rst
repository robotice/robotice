=================
Add support for new device
=================

Every device in Robotice must has own python module in $R_DRIVERS_DIR.

* sispm/__init__.py (for python 3 > is not required)
* sispm/sensosr.py
* sispm/actuator.py
* sispm/driver.py (optional standardized CLI for low level access is a suitable for debug or encapsulation the same code for sensor and actuator)

Sensor
=========

For every sensor which was found in `devices.yml` Robotice looking for python module in the $R_DRIVERS_DIR/<sensor_name> for example `$R_DRIVERS_DIR/sispm/sensor.py`. Sensor module must has method **get_data** with one argument *dict* sensor

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

Long running tasks
========

Why ? Sensor: I want average not actual value from one second.
Why ? Actuator: I want continuously blink with my diod.

Sensor
--------

Simple example of long running sensor with return average

.. code-block:: python

	from time import sleep
	import random

	def get_average(sensor):
	    average = 0
	    values = []

	    while len(values) <= 60:
	        values.append(random.randint(0,100))
	        sleep(1)

	    return reduce(lambda x, y: x + y, values) / len(values)

	def get_data(sensor):

	    output = get_average(sensor)

	    data = []

	    metric_format = "{0}.ave_{1}"

	    data.append(
	        (metric_format.format(sensor.get('name'), sensor.get("type").lower()), output,))

	    return data