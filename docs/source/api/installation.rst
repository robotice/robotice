
===
API
===

Robotice API is only for temporary usage. Its designed only for all-in-one solution where we need basic control via API only for local domain. From this API we can managing only one Robotice !.
This API hasn't any auth and is realy dangerous for public environment ! For full API please see Robotice Control Agent API which has full Auth and its designed for public environments.


Installation
------------

make file /srv/robotice/conf/api.conf and add content which is below.

.. code-block:: python

	[pipeline:api]
	pipeline = request_id faultwrap ssl versionnegotiation authurl authtoken context apiv1app


	[app:robotice.api]
	paste.app_factory = robotice.api.wsgi:app_factory
	robotice.app_factory = robotice.api.v1:API

here you can provide additionals config like a logging or binding


.. code-block:: python

	...

	bind_host=0.0.0.0
	bind_port=8004

add these packages into requirements.txt or manual install

.. code-block:: python

    eventlet==0.16.0
    greenlet==0.4.5
    Routes==2.0
    WebOb==1.4
    PasteDeploy>=1.5.0
    oslo.i18n>=1.0.0
    oslo.messaging>=1.4.0,!=1.5.0
    oslo.middleware>=0.1.0
    oslo.serialization>=1.0.0
    oslo.utils>=1.1.0


Run API
-------

In debug mode and see privided configuration.

.. code-block:: bash

    bin/robotice api run 0.0.0.0 8004 -d

    INFO (shell) Starting Robotice ReST API on 0.0.0.0:8004
    INFO (wsgi) Starting single process server
    DEBUG (log) (28759) wsgi starting up on http://0.0.0.0:8004/

note: please see api -h
note: if API not stared, run with -d argument and see error result. obviously missing any requirement 