
Managing settings via CLI
=========================

Listings
--------

throught devices, plans, systems, actions

.. code-block:: bash
    
    (robotice)root@control-single:/srv/robotice/service# ./bin/robotice conf list actions -d                                                                                                                          
    1:
      command: reactor.commit_action
      description: 'Long description for this action'
      id: 1
      name: 'Turn on light'
      options:
        args:
          device:
            device: sispm
            os_family: Arch
            port: 0
            socket: 4
          value: 1
        queue: reactor
      short_name: 'Light in kitchen'
    2:
      command: reactor.commit_action
      description: 'Long description for this action'
      id: 2
      name: 'Turn off light'
      options:
        args:
          device:
            device: sispm
            os_family: Arch
            port: 0
            socket: 4
          value: 0
        queue: reactor
      short_name: 'Light in kitchen'

GET
---

.. code-block:: bash

    (robotice)root@control-single:/srv/robotice/service# ./bin/robotice conf get systems box03.prd.pub.robotice.cz -d
    actuators:
      6:
        device: sispm1
        plan: water1
        socket: 2
      8:
        device: sispm1
        plan: light1
        socket: 4
    plan: 3000
    sensors:
      9:
        device: sispm1
        metric: socket1
        plan: water1
      10:
        device: sispm1
        metric: socket2
        plan: water1
      11:
        device: sispm1
        metric: socket3
        plan: light1
      12:
        device: sispm1
        metric: socket4
        plan: light1
      hygro1:
        device: hygro1
        metric: hygro_do
        plan: terra_humidity
    start: 2014-02-01 00:00:00

SET
---

.. code-block:: bash
    
    (robotice)root@control-single:/srv/robotice/service# ./bin/robotice conf set systems box03.prd.pub.robotice.cz:plan 4000 -d
    key box03.prd.pub.robotice.cz:plan was changed 
     3000 --> 4000    