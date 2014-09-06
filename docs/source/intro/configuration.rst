=================
Configuration
=================

Configuration - workers
=================

Root PATH for load workers is default to `/srv/robotice`. Here is expected one file per role in format yml.

Full example for the reasoner:
-----

.. code-block:: yaml

	cpu_arch: x86_64
	os_family: Debian
	system_name: box
	name: rabbitmq1.box.robotice.cz
	environment: dev
	debug: true
	broker: "amqp://robotice:robotice@localhost:5672//robotice"
	database:
	  engine: redis
	  host: localhost
	  port: 6379
	metering:
	  host: localhost
	  port: 8125
	  sample_rate: 1

You can override this path if will be set system variable `R_WORKERS_DIR`

Expected files:
-----

* <R_WORKERS_DIR>/config_monitor.yml
* <R_WORKERS_DIR>/config_reasoner.yml

*etc..*

Default is `/srv/robotice/`.

RabbitMQ or Redis:
=====

RabbitMQ is recomended, but Redis is a good alternative.

RabbitMQ
-----

.. code-block:: yaml

	broker: "amqp://robotice:robotice@localhost:5672//robotice"

*amqp://<user>:<password>@<host>:<port>/<virtual_host>*

Redis
-----

Redis is more suited for *'all in one'* environments especially for deployments on BB or RPi.

.. code-block:: yaml

	broker: "redis://localhost:6379/9"

*redis://<host>:<port>/<number>*

Configuration - psychical hardware
=================

You can override this path if will be set system variable `R_CONFIG_DIR`.

Default is `/srv/robotice/conf`.

Expected files:
-----

* <R_CONFIG_DIR>/devices.yml
* <R_CONFIG_DIR>/systems.yml
* <R_CONFIG_DIR>/plans.yml

Devices
-----

.. code-block:: yaml

	devices:
	- host: rabbitmq2
	  sensors:
	  - name: dummy2
	    device: dummy
	    type: dummy
	    port: bcm18  
	  - name: sispm1
	    device: sispm
	    port: 0
	  actuators:
	  - name: sispm1
	    device: sispm
	    port: 0
	    socket: 1
	  - name: sispm2
	    device: sispm
	    port: 0
	    socket: 2
	  - name: sispm3
	    device: sispm
	    port: 0
	    socket: 3
	  - name: sispm4
	    device: sispm
	    port: 0
	    socket: 4

Plans
-----

.. code-block:: yaml

	plans:
	- name: hklab_box1
	  description: simple test box
	  cycle: 1800
	  actuators:
	  - name: light1
	    cycles:
	    - value: 1
	      start: 6400
	      end: 80000
	  - name: water1
	    cycles:
	    - value: 0
	      start: 6400
	      end: 80000
	  - name: water2
	    cycles:
	    - start: 0
	      end: 59
	      value: 1
	  sensors:
	  - name: temp1
	    cycles:
	    - start: 0
	      end: 599
	      value_low: 0
	      value_high: 25
	    - start: 600
	      end: 1199
	      value_low: 30
	      value_high: 50
	    - start: 1200
	      end: 1800
	      value_low: 35
	      value_high: 55
	  - name: hygro1
	    cycles:
	    - start: 0
	      end: 1800
	      value_low: 1
	      value_high: 0
	  - name: water1
	    cycles:
	    - start: 0
	      end: 59
	      value: 1
	    - start: 60
	      end: 599
	      value: 0
	    - start: 600
	      end: 699
	      value: 1
	    - start: 700
	      end: 1399
	      value: 0
	    - start: 1400
	      end: 1499
	      value: 0
	    - start: 1500
	      end: 1739
	      value: 0
	    - start: 1740
	      end: 1800
	      value: 1


Systems
-----

.. code-block:: yaml

	systems:
	- name: rabbitmq2
	  plan: hklab_box1
	  start: 2014-02-01 00:00:00
	  actuators:
	  - plan: water1
	    device: sispm1
	    metric: socket1
	  - plan: light1
	    device: sispm1
	    metric: socket2
	  - plan: water2
	    device: sispm1
	    metric: socket3
	  sensors:
	  - plan: hygro1
	    device: hygro_case1_do
	    metric: hygro_do
	  - plan: light1
	    device: sispm1
	    metric: socket2
	  - plan: water2
	    device: sispm1
	    metric: socket3