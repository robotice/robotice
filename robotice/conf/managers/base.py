
from __future__ import absolute_import

"""
base object managers

"""

import sys
import logging

from robotice.common import importutils

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend

LOG = logging.getLogger(__name__)


class BaseManager(object):

    def app(self, role=None, default="reasoner"):
        """robotice app config
        """

        # lazy loading
        conf_mod = importutils.import_module("robotice.conf")

        if not role and default:
            return conf_mod.setup_app(default)

        return conf_mod.setup_app(role)

    def capp(self, name=None, default="reasoner"):
        """celery app
        """
        if default and name is None:
            mod = self.find_some_worker()
            return self.load_app(mod)

        conf = importutils.import_module("robotice.worker_%s" % name)

        return self.load_app(conf)

    def list(self, id):
        raise NotImplementedError

    def save(self, id, item):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError

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
