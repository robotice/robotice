.. _cli-test:

=================
Command Line Interface
=================


If you have problem with Robotice you can use cli for debugging.


Welcome !
-----

.. code-block:: bash

	python robotice-cli.py

.. code-block:: yaml

	usage: robotice-cli.py [-h] [-c CONF] [-w WORKERCONF] [-l NODEINFO]
	                       [-i INSPECT] [-s]

	     ______       _                _             
	    (_____ \     | |           _  (_)            
	     _____) )___ | |__   ___ _| |_ _  ____ _____ 
	    |  __  // _ \|  _ \ / _ (_   _) |/ ___) ___ |
	    | |  \ \ |_| | |_) ) |_| || |_| ( (___| ____|
	    |_|   |_\___/|____/ \___/  \__)_|\____)_____)
	    

	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONF, --conf CONF  default: /srv/robotice/conf
	  -w WORKERCONF, --workerconf WORKERCONF
	                        default: /srv/robotice
	  -l NODEINFO, --nodeinfo NODEINFO
	                        -l ubuntu1
	  -i INSPECT, --inspect INSPECT
	                        print worker configuration -i reasoner
	  -s, --status          print robotice status

Worker config
-----

.. code-block:: bash

	python robotice-cli.py -i reasoner

.. code-block:: yaml

	{
	  "system_name": "box",
	  "cpu_arch": "x86_64",
	  "name": "rabbitmq1.box.robotice.cz",
	  "database": {
	    "engine": "redis",
	    "host": "localhost",
	    "port": 6379
	  },
	  "broker": "amqp://robotice:robotice@localhost:5672//robotice",
	  "metering": {
	    "host": "localhost",
	    "sample_rate": 1,
	    "port": 8125
	  },
	  "environment": "dev",
	  "os_family": "Debian",
	  "debug": true,
	  "dsn": "http://##:##@host/number"
	}

Robotice status
-----

.. code-block:: bash
   
    python robotice-cli.py -s

.. code-block:: yaml


	        Monitor      ........   :-)
	        Planner      ........   :-)
	        Reasoner     ........   :-)
	        Reactor      ........   :-)
	    

	        Sensors      ........   2
	        Actuators    ........   9
	        Systems      ........   3
	        Plans        ........   1

Robotice node info
-----

.. code-block:: bash

    python robotice-cli.py --nodeinfo ubuntu1 | ubuntu1.box.robotice.cz

.. code-block:: yaml

    {'start': datetime.datetime(2014, 2, 1, 0, 0), 'sensors': [{'device': 'dummy1', 'metric': 'random1', 'plan': 'water_humidity1'}, {'device': 'hygro_case1_ao', 'metric': 'humidity', 'plan': 'water_humidity2'}], 'name': 'ubuntu1', 'plan': 'hklab_box1', 'actuators': [{'device': 'dummy1', 'metric': 'random', 'plan': 'water1'}, {'device': 'relay3', 'plan': 'light1'}, {'device': 'relay2', 'plan': 'temp1'}]}
    {'actuators': [{'device': 'relay', 'type': 'relay', 'name': 'relay1', 'port': 'P9_20'}], 'host': 'ubuntu1', 'sensors': [{'device': 'dummy', 'type': 'dummy', 'name': 'dummy2', 'port': 'bcm18'}, {'device': 'dummy', 'type': 'dummy', 'name': 'dummy1', 'port': 'bcm18'}]}
    {'actuators': [{'cycles': [{'start': 6400, 'end': 80000, 'value': 1}], 'name': 'light1'}, {'cycles': [{'start': 6400, 'end': 80000, 'value': 0}], 'name': 'water1'}, {'cycles': [{'start': 0, 'end': 59, 'value': 1}, {'start': 60, 'end': 599, 'value': 0}, {'start': 600, 'end': 699, 'value': 1}, {'start': 700, 'end': 1399, 'value': 0}, {'start': 1400, 'end': 1499, 'value': 0}, {'start': 1500, 'end': 1739, 'value': 0}, {'start': 1740, 'end': 1800, 'value': 1}], 'name': 'water2'}], 'sensors': [{'cycles': [{'start': 0, 'end': 599, 'value_high': 25, 'value_low': 0}, {'start': 600, 'end': 1199, 'value_high': 50, 'value_low': 30}, {'start': 1200, 'end': 1800, 'value_high': 55, 'value_low': 35}], 'name': 'temp1'}, {'cycles': [{'start': 0, 'end': 1800, 'value_high': 2000, 'value_low': 50}], 'name': 'hygro2'}, {'cycles': [{'start': 0, 'end': 1800, 'value_high': 0, 'value_low': 1}], 'name': 'hygro1'}, {'cycles': [{'start': 0, 'end': 899, 'value_high': 30, 'value_low': 20}, {'start': 900, 'end': 1800, 'value_high': 65, 'value_low': 35}], 'name': 'air_humidity1'}, {'cycles': [{'start': 0, 'end': 899, 'value_high': 30, 'value_low': 20}, {'start': 900, 'end': 1800, 'value_high': 65, 'value_low': 35}], 'name': 'terra_humidity1'}, {'cycles': [{'start': 0, 'end': 899, 'value': 1}, {'start': 900, 'end': 1800, 'value': 0}], 'name': 'light2'}, {'cycles': [{'start': 0, 'end': 59, 'value': 1}, {'start': 60, 'end': 599, 'value': 0}, {'start': 600, 'end': 699, 'value': 1}, {'start': 700, 'end': 1399, 'value': 0}, {'start': 1400, 'end': 1499, 'value': 0}, {'start': 1500, 'end': 1739, 'value': 0}, {'start': 1740, 'end': 1800, 'value': 1}], 'name': 'water1'}], 'description': 'simple test box', 'name': 'hklab_box1', 'cycle': 1800}
