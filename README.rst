Robotice monitoring
===============

Opensource monitoring, reasoning and acting framework.

`Documentation`_

`Video demostration`_

Usage
-----

App for distributed monitoring small devices like a BeagleBone black or Raspberry Pi.

Supported sensors:
-----

* `DHT11`_ / `DHT2302`_
* `TMP36`_
* `Hygro soil`_
* `relay_board`_
* `Sispm`_


Requirements
-----

* Python 2.6 / 2.7
* Celery
* database - Redis
* Graphite - Statsd (for Gauge)
* Service wrapper - Supervisor is recommended

Installation
------------

`Documentation`_


Show me in action
-----

.. image:: /docs/source/_static/imgs/show_me.gif

Read more
-----

.. _Website: http://www.robotice.cz
.. _Documentation: http://robotice.github.io/robotice/
.. _Video demostration: TODO
.. _Sispm: http://sispmctl.sourceforge.net/
.. _Hygro soil: /docs/source/_static/imgs/hygro.JPG
.. _DHT11: /docs/source/_static/imgs/dht11.jpg
.. _DHT2302: /docs/source/_static/imgs/dht2302.jpg
.. _TMP36: /docs/source/_static/imgs/tmp36.jpg
.. _relay_board: /docs/source/_static/imgs/relay_board.jpg
