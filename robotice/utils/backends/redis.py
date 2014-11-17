
from __future__ import absolute_import

import logging
import pickle

from robotice.utils.backends.base import KeyValueStoreBackend

LOG = logging.getLogger(__name__)

try:
    import redis
    from redis.exceptions import ConnectionError
except ImportError:                 # pragma: no cover
    redis = None                    # noqa
    ConnectionError = None          # noqa


class PickledRedis(redis.StrictRedis):
    """pickled redis connection
    """

    def hgetall(self, name):
        pickled_value = super(PickledRedis, self).hgetall(name)

        for key, value in pickled_value.iteritems():
            try:
                pickled_value[key] = pickle.loads(value)
            except Exception, e:
                pass
        return pickled_value

    def get(self, name):
        pickled_value = super(PickledRedis, self).get(name)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super(PickledRedis, self).set(name, pickle.dumps(value), ex, px, nx, xx)


class RedisBackend(PickledRedis, KeyValueStoreBackend):
    """ Robotice Redis backend
    """

    def __init__(self, host="localhost", port=6379, db=0, **kwargs):
        super(RedisBackend, self).__init__(host=host, port=port, db=db, **kwargs)
        
        self.host = host
        self.port = port
        self.db = db
