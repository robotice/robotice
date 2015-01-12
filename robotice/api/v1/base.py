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

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend
from oslo.utils import importutils

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


    def app(self, name=None, default=False):
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