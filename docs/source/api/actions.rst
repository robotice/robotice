
=======
Actions
=======

If you have *actions* dierctory in your plans path actions will be accessable from you API

.. code-block:: bash

    /srv/robotice/config/actions/my_actions.yml
    ...
    /srv/robotice/config/devices.yml
    /srv/robotice/config/plans.yml


Now you can define your actions into my_actions.yml

.. code-block:: yaml

    1:
      name: 'Turn light 4 on in the kitchen'
      short_name: 'Light in kitchen'
      description: 'Long description for this action'
      command: 'reactor.commit_action'
      options:
        queue: reactor
        args:
          device:
            os_family: "Arch"
            socket: 4
            device: sispm
            port: 0
          value: 1

    this_is_uuid:
      name: 'Turn light 4 off in the kitchen'
      short_name: 'Light in kitchen'
      description: 'Long description for this action'
      command: 'reactor.commit_action'
      options:
        queue: reactor
        args:
          device:
            os_family: "Arch"
            socket: 4
            device: sispm
            port: 0
          value: 0


navigate your browser to localhost:8004/action/list and see result

.. code-block:: bash

    root@samsung:~# http 10.10.10.23:8004/action/list
    HTTP/1.1 200 OK
    Content-Length: 611
    Content-Type: application/json; charset=UTF-8
    Date: Mon, 12 Jan 2015 19:22:54 GMT

    [
        {
            "command": "reactor.commit_action", 
            "description": "Long description for this action", 
            "id": 1, 
            "name": "Turn light 4 on in the kitchen", 
            "options": {
                "args": {
                    "device": {
                        "device": "sispm", 
                        "os_family": "Arch", 
                        "port": 0, 
                        "socket": 4
                    }, 
                    "value": 1
                }, 
                "queue": "reactor"
            }, 
            "short_name": "Light in kitchen"
        }
    ]

Why ?

Now do your actions !

.. code-block:: bash

    root@samsung:~# http POST 10.10.10.23:8004/action/do/1
    HTTP/1.1 200 OK
    Content-Length: 288
    Content-Type: application/json; charset=UTF-8
    Date: Mon, 12 Jan 2015 19:21:21 GMT

    {
        "action": {
            "command": "reactor.commit_action", 
            "description": "Long description for this action", 
            "id": 1, 
            "name": "Turn light 4 on in the kitchen", 
            "options": {
                "queue": "reactor"
            }, 
            "short_name": "Light in kitchen"
        }, 
        "state": "PENDING", 
        "task-id": "e2b8925a-fb68-4390-ae9f-da725ea4c53e"
    }

For more examplanation what you can do, see code below:

.. code-block:: python

    options = action.options
    args = options.pop("args")
    kwargs = options.pop("kwargs")

    result = app.send_task(
        command, args=args, kwargs=kwargs, **options)

For example:

.. code-block:: yaml

    command: 'reactor.commit_action'
    options:
      queue: reactor
      exchange: reactor
      args:
        device:
          os_family: "Arch"
          socket: 4
          device: sispm
          port: 0
        value: 0

will send this task:

.. code-block:: python

    send_task("reactor.commi_action", args=[{"os_family":"Arch", "socket":4, "device":"sispm", "port":0},0], queue="reactor", exhcange="reactor")