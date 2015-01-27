
from __future__ import absolute_import

"""
base object managers

"""

import os
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
import glob

LOG = logging.getLogger(__name__)

# for supporting hostname in key like box03.prd.pub.robotice.org
DELIMETER = ":"
RELOAD = False  # if true config will be reloaded on every read data


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

    def create(self, key, value):
        self._set(key, value, dump=True)

    def update(self, key, value):
        self._set(key, value, dump=True, create=False)

    def delete(self, key):
        self._del(key, dump=True)

    def set(self, key, value):
        """update conf
        """
        old_value = self._get(key)
        self._set(key, value, dump=True)
        self.load()
        new_value = self._get(key)
        LOG.debug("key %s was changed \n %s --> %s" % (key, old_value, new_value))
        if new_value != old_value:
            return True
        return False

    def _get(self, key, default={}, deliemeter=DELIMETER):
        """
        note: conf_api.get return tuple(result, '')
        """
        obj = conf_api.get(self.data, key, seps=deliemeter)[0]
        if not obj:
            LOG.debug("key %s not found in %s" % (key, self.data))
            return default
        return obj

    def _set(self, key, val, dic=None, deliemeter=DELIMETER, dump=False, create=True):
        """def set_(dic, path, val, seps=P.PATH_SEPS, strategy=None):"""

        dumped = False

        # find and update file
        for path in glob.glob(self._config()):
            _data = anyconfig.load(path)
            item = conf_api.get(_data, key, seps=deliemeter)[0]
            if item:
                conf_api.set_(_data, key, val, seps=deliemeter)
                if dump:
                    dumped = True
                    return self.dump(_data, path)

        if not dumped:
            if create:
                conf_api.set_(_data, key, val, seps=deliemeter)
                return self.dump(_data, glob.glob(self._config())[0])
            else:
                raise Exception("Key %s not found !" % (key))

    def _del(self, key, dic=None, deliemeter=DELIMETER, dump=False):
        """not ready yet !
        """

        removed = False

        name = key.split(deliemeter)[-1]
        key = ("%s" % deliemeter).join(key.split(deliemeter)[:-1])

        # find and delete
        for path in glob.glob(self._config()):
            _data = anyconfig.load(path)
            item = conf_api.get(_data, key, seps=deliemeter)[0]
            if name in item: 
                del item[name]
                result = self.set(key, item)
                return result

        if not removed:
            raise Exception("Key %s not found !" % (key))
        return True

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
        self._data = anyconfig.load(
            path or self._config(), ignore_missing=True)
        return self._data

    def _config(self):
        return os.path.join(os.environ["R_CONFIG_DIR"], self.config_path)

    @property
    def data(self):
        if RELOAD:
            return self.load()
        return self._data

class CeleryManager(object):

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
