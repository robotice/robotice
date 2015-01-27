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

from robotice.common.i18n import _
from robotice.common import importutils

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend

LOG = logging.getLogger(__name__)


class BaseController(object):
    """

    provide specific helpers for working with workers and celery tasks

    """

    def __init__(self, options):
        self.options = options

    def default(self, req, **args):
        raise exc.HTTPNotFound()

    def backend_configured(self, result):
        return not isinstance(result.backend, DisabledBackend)

    @property
    def app(self, role=None, default="reasoner"):
        """robotice app config
        """

        # lazy loading
        conf_mod = importutils.import_module("robotice.conf")

        if not role and default:
            return conf_mod.setup_app(default)

        return conf_mod.setup_app(role)

    def capp(self, name=None, default=False):
        """celery app
        """
        if default and name is None:
            mod = self.find_some_worker()
            return self.load_app(mod)

        conf = importutils.import_module("robotice.worker_%s" % name)

        return self.load_app(conf)

    def _get_task_args(self, body):
        """helper which return task args, kwargs and options
        """

        try:
            options = body
            if isinstance(body, basestring):
                options = json.loads(body)
            args = options.pop('args', [])
            kwargs = options.pop('kwargs', {})
        except Exception, e:
            raise exc.HTTPBadRequest(str(e))

        if not isinstance(args, (list, tuple)):
            try:
                args = args.values()
                return args, kwargs, options
            except Exception, e:
                raise e
            raise exc.HTTPBadRequest('args must be an array')

        return args, kwargs, options

    @staticmethod
    def load_app(module):
        """load celery app from config file
        """

        app = Celery(module.__name__)
        app.config_from_object(module)

        return app

    def find_some_worker(self):
        """ this method find first available worker
        """

        for worker in ["reasoner", "planer", "monitor", "reactor"]:

            try:
                conf = importutils.import_module("robotice.worker_%s" % worker)
                return conf                
            except ImportError:
                raise e

        return None

    @classmethod
    def create_resource(cls, options):
        """
        generic resource factory method.
        """

        return wsgi.Resource(cls(options))


class GenericController(BaseController):
    """

    generic controller

    """

    def __init__(self, options):
        super(GenericController, self).__init__(options)


    def index(self, req):
        """
        Returns a list of devices.

        ..code-block:: bash

            majklk@samsung:~ http GET http://10.10.10.23:8004/device/list
            HTTP/1.1 200 OK
            Content-Length: 627
            Content-Type: application/json; charset=UTF-8
            Date: Mon, 26 Jan 2015 23:59:24 GMT

            {
                "control-single.robotice.dev.mjk.robotice.cz": {
                    "actuators": {
                        "dummy1": {
                            "device": "dummy", 
                            "metric": "random", 
                            "port": "bcm18", 
                            "type": "dummy"
                        }
            ...

            }
        """

        manager = getattr(self.app, self.REQUEST_SCOPE, None)
        result = manager.list()
        return result

    def show(self, req, id):
        """get single object

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

        obj = None

        try:
            obj = getattr(self.app, self.REQUEST_SCOPE, None).get(id)
        except Exception, e:
            pass

        if obj is None:
            return {"id": id, "status": "404 - not found this action"}

        return obj

    def create(self, req, body={}):
    
        response = {"status": "ok"}
        LOG.debug(body)

        self.validate(body)

        try:
            obj = getattr(self.app, self.REQUEST_SCOPE, None).create(id, body)
        except Exception, e:
            response = {"status": "error", "errors": str(e)}

        return response

    def update(self, req, id=None, body={}):
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

        response = {"status": "ok"}

        self.validate(body)

        try:
            obj = getattr(self.app, self.REQUEST_SCOPE, None).update(id, body)
        except Exception, e:
            response = {"status": "error", "errors": str(e)}

        return response

    def delete(self, req, id):
        response = {"status": "ok"}
        LOG.error(id)
        try:
            obj = getattr(self.app, self.REQUEST_SCOPE, None).delete(id)
        except Exception, e:
            response = {"status": "error", "errors": str(e)}

        return response
    
    def validate(self, body, params=None):
        """helper which validate self.PARAMS and raise bad request
        """
        for param in params or getattr(self, "PARAMS", list()):
            if not param in body:
                LOG.debug(body)
                LOG.debug(id)
                raise exc.HTTPBadRequest("Missing required params %s" % param)