#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Task endpoint for Robotice v1 ReST API.
"""

import six
import json
import logging
from six.moves.urllib import parse
from webob import exc

from robotice.utils import serializers
from robotice.utils import tasks
from robotice.api import wsgi
from robotice.api.v1.base import BaseController

from robotice.common.i18n import _

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend

LOG = logging.getLogger(__name__)

import glob
from yaml import load, dump, safe_dump

CONFIG_DIR = "/srv/robotice/config"
ACTION_DIR = "actions"


def load_actions():
    """load and return all actions from local storage
    """

    path = "/".join([CONFIG_DIR, ACTION_DIR])

    actions = []

    for path in glob.glob("/".join([path, '*.yml'])):
        try:
            f = open(path, 'r')
            raw_data = load(f)
            for id, action in raw_data.iteritems():
                action["id"] = id
                actions.append(action)
        except Exception, e:
            raise e

    return actions


def get_action(action_id):
    """return action if is founded
    """

    for action in load_actions():

        if str(action["id"]) == str(action_id):
            return action

    return None

def set_action(id, action):
    """save action to disk

    TODO: recursive dump with indentation

    """

    path = "/".join([CONFIG_DIR, ACTION_DIR])
    paths = glob.glob("/".join([path, '*.yml']))

    created = True

    for path in paths:
        try:
            f = open(paths[0], 'r')
            raw_data = load(f)
            f.close()
            for _id, _action in raw_data.iteritems():
                if str(_id) == str(id):
                    _old = _action
                    try:
                        action["options"] = load(action["options"])
                    except Exception, e:
                        raise e
                    _old.update(action)
                    raw_data[_id] = _old
                    if not "id" in action:
                        action["id"] = id

                    with open(path, 'w') as yaml_file:
                        safe_dump(raw_data, yaml_file, default_flow_style=False, allow_unicode=True)
                        created = False
        except Exception, e:
            raise e

    if created:

        try:
            f = open(paths[0], 'r')
            raw_data = load(f)
            f.close()
            raw_data[id] = action

            with open(paths[0], 'w') as yaml_file:
                safe_dump(raw_data, yaml_file, default_flow_style=False)
        except Exception, e:
          raise e

    return True


class ActionController(BaseController):

    """

    load actions from local storage and prodive API for managing it

    """

    # Define request scope (must match what is in policy.json)
    REQUEST_SCOPE = 'actions'

    def action_list(self, req):
        """
        Returns a list of actions.

        ..code-block:: bash

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

        """

        result = load_actions()

        return result

    def do_action(self, req, action_id, body={}):
        """Execute a action by name(uuid) (doesn't require task sources)

        **Example request**:

        ..code-block:: bash

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

        """

        action = get_action(action_id)

        LOG.error(action)

        app = self.app(default=True)

        args, kwargs, options = self._get_task_args(action.get("options"))
        command = action.get("command", None)
        LOG.error(args)
        LOG.debug("Invoking task '%s' with '%s' and '%s'",
                  command, args, kwargs)

        result = app.send_task(
            command, args=args, kwargs=kwargs, **options)
        response = {'task-id': result.task_id}

        response["action"] = action

        if self.backend_configured(result):
            response.update(state=result.state)

        return response

    def action_set(self, req, id, body={}):
        """create or update action via API

        {
            id: 1
            name: foo,
            command: reactor.commit_action,
            options:
              device: foo
              value: 1
        }

        """

        def validate(body):

            if not "id" or "command" in body:
                raise exc.HTTPBadRequest("Missing required params id or command")

        LOG.error(body)

        response = {"status": "ok"}
        try:
            action = set_action(id, body)
        except Exception, e:
            raise e
            response = {"status": "fail", "exception": "error"}
            return response

        return response


    def action_get(self, req, id):
        """get single action

        response:

        ..code-block:: json
            {
                id: 1
                name: foo,
                command: reactor.commit_action,
                options:
                  device: foo
                  value: 1
            }

        """

        action = None

        try:
            action = get_action(id)
        except Exception, e:
            pass

        if action is None:
            return {"id": id, "status": "404 - not found this action"}

        return action
