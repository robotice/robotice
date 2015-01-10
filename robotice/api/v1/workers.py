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
Worker endpoint for Robotice v1 ReST API.
"""

import six
import json
import logging
from six.moves.urllib import parse
from webob import exc

from robotice.utils import serializers
from robotice.utils import tasks
from robotice.api import wsgi

from robotice.common.i18n import _

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend

LOG = logging.getLogger(__name__)


class WorkerController(object):

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
    REQUEST_SCOPE = 'workers'

    def __init__(self, options):
        self.options = options

    def default(self, req, **args):
        raise exc.HTTPNotFound()
    """
    def _index(self, req):
        filter_whitelist = {
            'status': 'mixed',
            'name': 'mixed',
            'action': 'mixed',
            'tenant': 'mixed',
            'username': 'mixed',
            'owner_id': 'mixed',
        }
        whitelist = {
            'limit': 'single',
            'marker': 'single',
            'sort_dir': 'single',
            'sort_keys': 'multi',
            'show_deleted': 'single',
            'show_nested': 'single',
        }
        params = req.params
        filter_params = req.params

        show_deleted = False
        if rpc_api.PARAM_SHOW_DELETED in params:
            params[rpc_api.PARAM_SHOW_DELETED] = param_utils.extract_bool(
                params[rpc_api.PARAM_SHOW_DELETED])
            show_deleted = params[rpc_api.PARAM_SHOW_DELETED]
        show_nested = False
        if rpc_api.PARAM_SHOW_NESTED in params:
            params[rpc_api.PARAM_SHOW_NESTED] = param_utils.extract_bool(
                params[rpc_api.PARAM_SHOW_NESTED])
            show_nested = params[rpc_api.PARAM_SHOW_NESTED]
        # get the with_count value, if invalid, raise ValueError
        with_count = False
        if req.params.get('with_count'):
            with_count = param_utils.extract_bool(
                req.params.get('with_count'))

        if not filter_params:
            filter_params = None

        stacks = self.rpc_client.list_stacks(req.context,
                                             filters=filter_params,
                                             tenant_safe=tenant_safe,
                                             **params)

        args, kwargs, options = self.get_task_args()
        LOG.debug("Invoking task '%s' with '%s' and '%s'",
                  taskname, args, kwargs)
        result = app.send_task(
            taskname, args=args, kwargs=kwargs, **options)
        response = {'task-id': result.task_id}

        if self.backend_configured(result):
            response.update(state=result.state)

        return self.response(response)
    """

    @staticmethod
    def backend_configured(result):
        return not isinstance(result.backend, DisabledBackend)

    def worker(self, name):
        app = Celery(name)

        conf = __import__("robotice.worker_%s" % name)

        from robotice import worker_reactor

        app.config_from_object(worker_reactor)

        app.autodiscover_tasks('robotice.%s' % name)

        LOG.error(app.tasks)

        return app

    def worker_list(self, req, role=None):
        """
List workers
**Example request**:
.. sourcecode:: http
  GET /api/workers HTTP/1.1
  Host: localhost:5555
**Example response**:
.. sourcecode:: http
  HTTP/1.1 200 OK
  Content-Length: 119
  Content-Type: application/json; charset=UTF-8
  {
      "celery@worker1": {
          "completed_tasks": 0,
          "concurrency": 4,
          "queues": [
              "celery"
          ],
          "running_tasks": 0,
          "status": true
      },
      "celery@worker2": {
          "completed_tasks": 0,
          "concurrency": 4,
          "queues": [],
          "running_tasks": 0,
          "status": false
      }
  }
:reqheader Authorization: optional OAuth token to authenticate
:statuscode 200: no error
:statuscode 401: unauthorized request
        """

        app = self.worker(role)
        events = app.events.State()

        response = app.control.inspect().stats()

        return response


class WorkerSerializer(serializers.JSONResponseSerializer):

    """Handles serialization of specific controller method responses."""

    def _populate_response_header(self, response, location, status):
        response.status = status
        response.headers['Location'] = location.encode('utf-8')
        response.headers['Content-Type'] = 'application/json'
        return response

    def create(self, response, result):
        self._populate_response_header(response,
                                       result['stack']['links'][0]['href'],
                                       201)
        response.body = self.to_json(result)
        return response


def create_resource(options):
    """
    Task resource factory method.
    """
    deserializer = wsgi.JSONRequestDeserializer()
    serializer = WorkerSerializer()
    return wsgi.Resource(WorkerController(options), deserializer, serializer)
