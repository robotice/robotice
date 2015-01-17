.. _cli-test:

======================
Command Line Interface
======================

Robotice Welcome!
----------------

.. code-block:: bash

	(robotice)root@control-single:/srv/robotice/service# bin/robotice -h

.. code-block:: yaml

	usage: robotice [-r ROLE] [--version] [-d] [-v]

	 ______       _                _             
	(_____ \     | |           _  (_)            
	 _____) )___ | |__   ___ _| |_ _  ____ _____ 
	|  __  // _ \|  _ \ / _ (_   _) |/ ___) ___ |
	| |  \ \ |_| | |_) ) |_| || |_| ( (___| ____|
	|_|   |_\___/|____/ \___/  \__)_|\____)_____)    0.2.54

	Optional arguments:
	  -r ROLE, --role ROLE  role [reactor,monitor, ..]
	  --version             Shows the Robotice version.
	  -d, --debug           Defaults to env[ROBOTICE_DEBUG].
	  -v, --verbose         Print more verbose output.

	See "robotice help COMMAND" for help on a specific command.


Robotice inspect
----------------

is only ping to all workers

.. code-block:: bash
   
	(robotice)root@control-single:/srv/robotice/service# bin/robotice reactor inspect -d
	+------------------------------------------------------+--------+
	|                        Worker                        | Status |
	+------------------------------------------------------+--------+
	| reasoner@control-single.robotice.dev.mjk.robotice.cz |   ok   |
	| reactor@control-single.robotice.dev.mjk.robotice.cz  |   ok   |
	| planner@control-single.robotice.dev.mjk.robotice.cz  |   ok   |
	| monitor@control-single.robotice.dev.mjk.robotice.cz  |   ok   |
	+------------------------------------------------------+--------+


Check config
-----

.. code-block:: bash

	robotice reactor config

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


Robotice run
----------------

.. code-block:: bash
   
	(robotice)root@control-single:/srv/robotice/service# bin/robotice run reactor
	
	(robotice)root@control-single:/srv/robotice/service# bin/robotice run monitor -d

	(robotice)root@control-single:/srv/robotice/service# bin/robotice run api
