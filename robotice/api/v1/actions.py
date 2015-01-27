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
from robotice.api.v1.base import GenericController

from robotice.common.i18n import _

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend

LOG = logging.getLogger(__name__)

from robotice.conf.managers import actions


class ActionController(GenericController):

    """

    load actions from local storage and prodive API for managing it

    """

    # Define request scope (must match what is in policy.json)
    REQUEST_SCOPE = 'actions'


    def do(self, req, id, body={}):
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

        action = actions.get(id)

        LOG.error(action)

        app = self.capp(default=True)

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