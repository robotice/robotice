
from __future__ import absolute_import

"""
base object managers

"""

import sys
import logging

from robotice.common import importutils

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

    def list(self, id):
        raise NotImplementedError

    def save(self, id, item):
        raise NotImplementedError

    def get(self, id):
        raise NotImplementedError
