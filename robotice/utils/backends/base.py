
from __future__ import absolute_import

import logging

LOG = logging.getLogger(__name__)


class BaseBackend(object):
    """Base Backend
    """

    def get(self, key):
        raise NotImplementedError('Must implement the get method.')

    def mget(self, keys):
        raise NotImplementedError('Does not support get_many')

    def hmset(self, key, value):
        raise NotImplementedError('DB Backend must have implemented hmset method.')

    def set(self, key, value):
        raise NotImplementedError('Must implement the set method.')

    def delete(self, key):
        raise NotImplementedError('Must implement the delete method')


class KeyValueStoreBackend(BaseBackend):
    pass