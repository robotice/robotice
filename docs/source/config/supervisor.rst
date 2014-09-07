=================
Supervisor Configuration
=================

Reasoner Service
-----

.. code-block:: bash

	[program:robotice_reasoner]
	directory=/srv/robotice/service/robotice
	environment=PATH="/srv/robotice/bin;/srv/robotice/service"
	command=/srv/robotice/bin/celery worker -s /srv/robotice/logs/celerybeat-schedule -B -E -Q reasoner,reasoner_rabbitmq1.box.robotice.cz,default --config=worker_reasoner --hostname=reasoner@rabbitmq1.box.robotice.cz --loglevel=INFO --concurrency=1
	user=robotice
	stdout_logfile=/srv/robotice/logs/robotice_reasoner.log
	stderr_logfile=/srv/robotice/logs/robotice_reasoner.log
	autostart=true
	autorestart=true
	startsecs=10
	stopwaitsecs=600

Monitor Service
-----

.. code-block:: bash

	[program:robotice_monitor]
	directory=/srv/robotice/service/robotice
	environment=PATH="/srv/robotice/bin"
	command=/srv/robotice/bin/celery worker -E -Q monitor,monitor_rabbitmq1.box.robotice.cz,default --config=worker_monitor --hostname=monitor@rabbitmq1.box.robotice.cz --loglevel=INFO --concurrency=1
	user=robotice
	stdout_logfile=/srv/robotice/logs/robotice_monitor.log
	stderr_logfile=/srv/robotice/logs/robotice_monitor.log
	autostart=true
	autorestart=true
	startsecs=10
	stopwaitsecs=600
