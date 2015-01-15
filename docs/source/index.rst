.. Robotice documentation master file, created by

========================
Robotice's documentation
========================

Robotice is autonomous agent-based system to solve common problems.

* ICT Service Monitoring - React to hardware and load problems by integration with opensource monitoring and configuration management frameworks.
* Security and survailance - Interact with cameras to capture and evaluate the data for alarms or other actions.
* Gardening Automation - Integrate various hardware sensors and actuators to support gardening automation.

.. toctree::
   :maxdepth: 2

Overview
===========

* :doc:`Robotice Overview <intro/overview>`
* :doc:`Screenshots <intro/screenshot>`
* :doc:`Screencasts <intro/screencast>`

Installation
===========

* :doc:`Installation by SaltStack<install/salt>`
* Manual installation

Configuration
===========

* :doc:`Agents <config/worker>`
* :doc:`Environment <config/environment>`
* :doc:`Management <config/supervisor>`
*  :doc:`Settings module <robotice/settings>`

Robotice Support
===========

  :doc:`CLI <support/cli>`
  :doc:`Simple manipulation through CLI <support/config>`

Robotice API
===========

*  :doc:`Installation and setup <api/installation>`
*  :doc:`Basic usage <api/usage>`
*  :doc:`Actions <api/actions>`

Supported Hardware
===========

Single board computers
-----

* Any x86/64 machine
* :doc:`Raspberry Pi <hardware/pi>`
* :doc:`BeagleBone Black<hardware/bb>`
* :doc:`Udoo <hardware/udoo>`

Sensors / Actuators
-----

* :doc:`Hygro soil <hardware/hygro>`
* :doc:`DHT <hardware/dht>`
* :doc:`Sispm <hardware/sispm>`
* :doc:`Relay <hardware/relay>`
* :doc:`TMP36 <hardware/tmp36>`
* :doc:`CDS <hardware/cds>`
* :doc:`TSL2561 <hardware/tls>`
* :doc:`Liquid Flow <hardware/liquid_flow>`
* :doc:`Current Sensor - 30A<hardware/current_sensor>`



:doc:`How i can add support for new device? <contrib/new_device>`

Contribution
===========

* :doc:`Source code <contrib/git>`
* :doc:`Add support for new device <contrib/new_device>`
* :doc:`Contributors <contrib/contributors>`

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

|Build Status| |License badge|

.. |Build Status| image:: https://travis-ci.org/robotice/robotice.svg?branch=master
    :target: https://travis-ci.org/robotice/robotice
.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat