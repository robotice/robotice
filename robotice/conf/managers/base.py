
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

import anyconfig
from anyconfig import api as conf_api
from anyconfig.mergeabledict import MergeableDict
import pyaml
import types

LOG = logging.getLogger(__name__)

DELIMETER = ":" # for supporting hostname in key like box03.prd.pub.robotice.org
RELOAD = True # if true config will be reloaded on every read data

def p(self):
    """recall pprint
    """
    data = self.convert_to(self)
    return pyaml.pprint(data)

class ManagerInterface(object):

    def list(self, key):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError


class BaseConfigManager(ManagerInterface):
    """ base config manager

    common operations for config files

    :param:config_path or as own property
    """
    
    def __init__(self, path=None, *args, **kwargs):
        self.load(path)
        super(BaseConfigManager, self).__init__(*args, **kwargs)

    def list(self):
        """load and return all items from local storage
        """
        return self._get("")

    def get(self, key):
        """load and return all items from local storage
        """
        return self._get(key)

    def set(self, key, value):
        """update conf
        """
        old_value = self._get(key)
        self._set(key, value, dump=True)
        new_value = self._get(key)
        return "key %s was changed \n %s --> %s" % (key, old_value, new_value)

    def _get(self, key, default={}, deliemeter=DELIMETER):
        """
        note: conf_api.get return tuple(result, '')
        """
        obj = conf_api.get(self.data, key, seps=deliemeter)[0]
        if not obj:
            LOG.debug("key %s not found in %s" % (key, self.data))
            return default
        return self.wrap(obj)

    def _set(self, key, val, dic=None, deliemeter=DELIMETER, dump=False):
        """def set_(dic, path, val, seps=P.PATH_SEPS, strategy=None):"""

        conf_api.set_(dic or self.data, key, val, seps=deliemeter)
        
        if dump:
            return self.dump(self.data, self._config)

    def dump(self, data, path):
        """dump data to file
        """

        with open(path, "w") as f:

            if isinstance(data, MergeableDict):
                pyaml.dump(data.convert_to(data), f)
            else:
                pyaml.dump(data, f)
    
    def load(self, path=None):
        """return loaded data as MergeableDict
        """
        self._data = anyconfig.load(path or self._config)
        return self._data

    @property
    def _config(self):
        return getattr(self, "config_path", "")

    @property
    def data(self):
        if RELOAD:
            return self.load()
        return self._data

    def wrap(self, obj):
        """only wrap returned object for common manipulate for example pprint method
        """
        if isinstance(obj, MergeableDict):
            obj.p = types.MethodType( p, obj )
        return obj

    def __call__(self, *args, **kwargs):
        """load config before using
        """
        super(BaseConfigManager, self).__call__(*args, **kwargs)


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
