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


class TaskController(BaseController):

    """
Execute a task by name (doesn't require task sources)
**Example request**:
.. sourcecode:: http
  POST /api/task/send-task/tasks.add HTTP/1.1
  Accept: application/json
  Accept-Encoding: gzip, deflate, compress
  Content-Length: 16
  Content-Type: application/json; charset=utf-8
  Host: localhost:5555
  {
      "args": [1, 2]
  }
**Example response**:
.. sourcecode:: http
  HTTP/1.1 200 OK
  Content-Length: 71
  Content-Type: application/json; charset=UTF-8
  {
      "state": "SUCCESS",
      "task-id": "c60be250-fe52-48df-befb-ac66174076e6"
  }
:query args: a list of arguments
:query kwargs: a dictionary of arguments
:reqheader Authorization: optional OAuth token to authenticate
:statuscode 200: no error
:statuscode 401: unauthorized request
:statuscode 404: unknown task
        """
    # Define request scope (must match what is in policy.json)
    REQUEST_SCOPE = 'tasks'

    def __init__(self, options):
        self.options = options

    def default(self, req, **args):
        raise exc.HTTPNotFound()

    def task_list(self, req, role, worker=None, type=None, limit=None, state=None):
        """
        Returns a list of celery tasks.
        """

        limit = limit and int(limit)
        worker = worker if worker != 'All' else None
        type = type if type != 'All' else None
        state = state if state != 'All' else None

        app = self.app(role)

        events = app.events.State()

        result = []
        for task_id, task in tasks.iter_tasks(
                events, limit=limit, type=type,
                worker=worker, state=state):
            task = task.as_dict()
            task.pop('worker')
            result.append((task_id, task))

        return result

    def send_task(self, req, role=None, taskname=None, body={}):
        """Execute a task by name (doesn't require task sources)
        **Example request**:
        .. sourcecode:: http
          http POST 10.10.10.23:8004/task/send/reactor/reactor.commit.action queue=reactor args:='[{"os_family":"Arch","socket":4,"device":"sispm","port":0},0]' queue=reactor
          POST /api/task/send-task/tasks.add HTTP/1.1
          Accept: application/json
          Accept-Encoding: gzip, deflate, compress
          Content-Length: 16
          Content-Type: application/json; charset=utf-8
          Host: localhost:5555
          {
              "args": [1, 2]
          }
        **Example response**:
        .. sourcecode:: http
          HTTP/1.1 200 OK
          Content-Length: 71
          Content-Type: application/json; charset=UTF-8
          {
              "state": "SUCCESS",
              "task-id": "c60be250-fe52-48df-befb-ac66174076e6"
          }
        :query args: a list of arguments
        :query kwargs: a dictionary of arguments
        :reqheader Authorization: optional OAuth token to authenticate
        :statuscode 200: no error
        :statuscode 401: unauthorized request
        :statuscode 404: unknown task
        """

        app = self.app(role)

        args, kwargs, options = self._get_task_args(body)
        LOG.debug("Invoking task '%s' with '%s' and '%s'",
                  taskname, args, kwargs)

        result = app.send_task(
            taskname, args=args, kwargs=kwargs, **options)
        response = {'task-id': result.task_id}

        if self.backend_configured(result):
            response.update(state=result.state)

        return response

    def task_result(self, req, role, task_id):
        """
        Get a task result
        **Example request**:
        .. sourcecode:: http
          GET /task/result/rector/c60be250-fe52-48df-befb-ac66174076e6 HTTP/1.1
          Host: localhost:5555
        **Example response**:
        .. sourcecode:: http
          HTTP/1.1 200 OK
          Content-Length: 84
          Content-Type: application/json; charset=UTF-8
          {
              "result": 3,
              "state": "SUCCESS",
              "task-id": "c60be250-fe52-48df-befb-ac66174076e6"
          }
        :reqheader Authorization: optional OAuth token to authenticate
        :statuscode 200: no error
        :statuscode 401: unauthorized request
        :statuscode 503: result backend is not configured
        """
        result = AsyncResult(task_id)

        if not self.backend_configured(result):
            raise exc.HTTPBadRequest(
                "backend disabled ! maybe set CELERY_RESULT_BACKEND fix this issue")
        response = {'task-id': task_id, 'state': result.state}
        if result.ready():
            if result.state == states.FAILURE:
                response.update({'result': result.result,
                                 'traceback': result.traceback})
            else:
                response.update({'result': result.result})

        return response

    def task_types(self, req, role):

        seen_task_types = self.app(role).events.state.task_types()

        response = {}
        response['task-types'] = seen_task_types

        return response

    def task_info(self, req, role, task_id):
        """
        Get a task info
        **Example request**:
        .. sourcecode:: http
          GET /task/info/reactor/91396550-c228-4111-9da4-9d88cfd5ddc6 HTTP/1.1
          Accept: */*
          Accept-Encoding: gzip, deflate, compress
          Host: localhost:5555
        **Example response**:
        .. sourcecode:: http
          HTTP/1.1 200 OK
          Content-Length: 575
          Content-Type: application/json; charset=UTF-8
          {
              "args": "[2, 2]",
              "client": null,
              "clock": 25,
              "eta": null,
              "exception": null,
              "exchange": null,
              "expires": null,
              "failed": null,
              "kwargs": "{}",
              "name": "tasks.add",
              "received": 1400806241.970742,
              "result": "'4'",
              "retried": null,
              "retries": null,
              "revoked": null,
              "routing_key": null,
              "runtime": 2.0037889280356467,
              "sent": null,
              "started": 1400806241.972624,
              "state": "SUCCESS",
              "succeeded": 1400806243.975336,
              "task-id": "91396550-c228-4111-9da4-9d88cfd5ddc6",
              "timestamp": 1400806243.975336,
              "traceback": null,
              "worker": "celery@worker1"
          }
        :reqheader Authorization: optional OAuth token to authenticate
        :statuscode 200: no error
        :statuscode 401: unauthorized request
        :statuscode 404: unknown task
        """

        app = self.app(role)
        events = app.events.State()

        task = tasks.get_task_by_id(events, task_id)
        if not task:
            raise exc.HTTPNotFound("Unknown task '%s'" % task_id)
        response = {}
        for name in task._fields:
            if name not in ['uuid', 'worker']:
                response[name] = getattr(task, name, None)
        response['task-id'] = task.uuid
        response['worker'] = task.worker.hostname

        return response
