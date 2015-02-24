|Build Status| |Coverage Status| |License badge|

Robotice Agent System
=====================

Opensource microframework for monitoring, reasoning and acting.


Use cases
---------

* automation for periodic tasks like a turn on heating every day in 7:00
* planning through human readable yaml files like a hold temperature between 20° - 30° every day from 7AM to 8AM
* continuous measuring, monitoring
* reasoning (simple conditions or fuzzy in FCL format)
* working well with SBC(single-board computes) like a BeagleBone black or Raspberry Pi

Why ?
-----

Robotice is small and simple Python daemon based on the Celery project which has support for many result backends(AMQP, Redis, Mongo, ..) with many features for communication in real time.
It's designed for distributed environments and every component would be installed on the another host or can be started as all-in-one solution without requisite to internet connection. Robotice is modular from core and support for all devices is through driver and configurable 

Where ?
-------

In the House, garden, garage or anywhere else..

`Documentation`_

Usage
-----

* Read documentation and install Robotice
* make a plan
* bin/robotice

Supported sensors:
------------------

* DHT family
* TMP36
* Hygro soil
* Relay Board
* Sispm

visit `devices`_

Supported architectures:
------------------------

* ARMv6, ARMv7
* x86, x64

Requirements
------------

* Python 2.6 / 2.7
* Celery
* database - Redis
* Graphite - Statsd (for Gauge)
* Service wrapper - Supervisor is recommended

Installation
------------

.. code-block:: python
    
    pip install robotice

    robotice.py run reasoner -B -d --loglevel=info

    robotice.py run reactor


Show me in action
-----------------

.. image:: /docs/source/_static/imgs/show_me.gif

Read more
---------

* http://intro.robotice.org/

Contribution
------------

* Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
* Fork https://github.com/robotice/robotice on GitHub to start making your changes to the **develop** branch.
* Write a test which shows that the bug was fixed or that the feature works as expected.
* Make sure to add yourself to the `contributors`_ file.
* Send a pull request

.. _Website: http://www.robotice.cz
.. _Documentation: docs.robotice.org
.. _devices: https://github.com/robotice-devices
.. _Video Demonstration: TODO
.. _contributors: https://github.com/robotice/robotice/blob/develop/docs/source/contrib/contributors.rst

.. |Build Status| image:: https://travis-ci.org/robotice/robotice.svg?branch=master
    :target: https://travis-ci.org/robotice/robotice
.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
.. |Coverage Status| image:: https://coveralls.io/repos/robotice/robotice/badge.png
      :target: https://coveralls.io/r/robotice/robotice

