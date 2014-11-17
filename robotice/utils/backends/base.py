
from __future__ import absolute_import

import logging

LOG = logging.getLogger(__name__)


class BaseBackend(object):
    """Base Backend
    """

    @property
    def database(self):
        """return db instance with available two methods get(key) and set(key, value)
        """
        raise NotImplementedError

    def update_or_create(self, obj, key):
        """method save object or iterable into db
        """
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError('Must implement the get method.')

    def mget(self, keys):
        raise NotImplementedError('Does not support get_many')

    def hmset(self, key, value):
        raise NotImplementedError('Must implement the set method.')

    def set(self, key, value):
        raise NotImplementedError('Must implement the set method.')

    def delete(self, key):
        raise NotImplementedError('Must implement the delete method')


class KeyValueStoreBackend(BaseBackend):
    pass