=================
Worker Configuration
=================

Root PATH for load workers defaults to `/srv/robotice`. Here is expected one file per role in format yml.

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

You can override this path by settings system variable `R_WORKER_DIR`.

Expected files:
-----

* <R_WORKER_DIR>/config_monitor.yml
* <R_WORKER_DIR>/config_reasoner.yml

*etc..*

Defaults to `/srv/robotice/`.

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

Sentry logging:
=====

Robotice supports logging to [Sentry]_. `dsn` key must be specified in worker configuration file and [Raven]_ lib is installed.

Raven DSN
-----

.. code-block:: yaml

    dsn: http://public:private@host/project

More about loggin, read [Raven]_ and [Sentry]_ documentation.

Graphite / Statsd:
=====

Key metering representing metric backend for Robotice.

Statsd configuration
-----

.. code-block:: yaml

	metering:
	  host: localhost
	  port: 8125
	  sample_rate: 1

For more information about Graphite metering used in Robotice, read [Graphite]_ and [Statsd]_ documentation.

.. [Raven] http://raven.readthedocs.org/en/latest/
.. [Sentry] https://getsentry.com/welcome/
.. [Statsd] https://github.com/etsy/statsd.git
.. [Graphite] http://graphite.wikidot.com/
