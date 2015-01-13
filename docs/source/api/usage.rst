
======
Usage
======

Run API
-------

In debug mode ans see privided configuration.

.. code-block:: bash

    bin/robotice api run 0.0.0.0 8004 -d

    INFO (shell) Starting Robotice ReST API on 0.0.0.0:8004
    INFO (wsgi) Starting single process server
    DEBUG (log) (28759) wsgi starting up on http://0.0.0.0:8004/

note: please see api -h


Task Send
---------

POST /task/send/{role}/{task_name}

.. code-block:: bash

    http POST 10.10.10.23:8004/task/send/reactor/reactor.commit_action queue=reactor args:='[{"os_family":"Arch","socket":4,"device":"sispm","port":0},0]'

.. code-block:: bash

    HTTP/1.1 200 OK
    Content-Length: 71
    Content-Type: application/json; charset=UTF-8
    Date: Sat, 10 Jan 2015 14:58:18 GMT

    {
        "state": "PENDING", 
        "task-id": "4a78b96d-96d2-4b42-a468-3c6ebf19d475"
    }

Task Info
---------

.. code-block:: bash
  
    GET /task/info/{role}/{task_id}
    
.. code-block:: bash
    
    http POST 10.10.10.23:8004/task/info/reactor/4a78b96d-96d2-4b42-a468-3c6ebf19d475

Task Result
---------

.. code-block:: bash
    
    GET /task/result/{role}/{task_id}

.. code-block: bash
    http POST 10.10.10.23:8004/task/info/reactor/4a78b96d-96d2-4b42-a468-3c6ebf19d475