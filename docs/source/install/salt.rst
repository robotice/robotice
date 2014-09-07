=================
Salt installation
=================

Sample pillars

Robotice controller node
-----

.. code-block:: yaml

    robotice:
      planner:
        enabled: true
        broker:
          engine: rabbitmq
          user: robotice
          password: nksfdfdewe3234
          host: localhost
          port: 5672
          virtual_host: /robotice
        database:
          engine: redis
          host: localhost
          port: 6379
      reasoner:
        enabled: true
        plan:
          source: git
          address: 'git@repo.domain.com:robotice/plan-default.git'
          rev: 'develop'
        broker:
          engine: rabbitmq
          user: robotice
          password: nksfdfdewe3234
          host: localhost
          virtual_host: /robotice
        database:
          engine: redis
          host: localhost
          port: 6379
        metering:
          engine: statsd
          host: localhost
          port: 8125
          sample_rate: 1

Robotice monitor node
-----

.. code-block:: yaml


      monitor:
        enabled: true
        broker:
          engine: rabbitmq
          user: robotice
          password: nksfdfdewe3234
          host: localhost
          virtual_host: /robotice
        database:
          engine: redis
          host: localhost
          port: 6379
        devices:
        - sispm
        - dht
        - relay
      reactor:
        enabled: true
        database:
          engine: redis
          host: localhost
          port: 6379
        broker:
          engine: rabbitmq
          user: robotice
          password: nksfdfdewe3234
          host: localhost
          virtual_host: /robotice
        devices:
        - sispm
        - relay


Robotice controller node with redis broker
-----

.. code-block:: yaml

    robotice:
      planner:
        enabled: true
        broker:
          engine: redis
          host: localhost
          port: 6379
          number: 0
        database:
          engine: redis
          host: localhost
          port: 6379
          number: 1
      reasoner:
        enabled: true
        plan:
          source: git
          address: 'git@repo.domain.com:robotice/plan-default.git'
          rev: 'develop'
        broker:
          engine: redis
          host: localhost
          port: 6379
          number: 0
        database:
          engine: redis
          host: localhost
          port: 6379
          number: 1
        metering:
          engine: statsd
          host: localhost
          port: 8125
          sample_rate: 1
