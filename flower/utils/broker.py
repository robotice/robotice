from __future__ import absolute_import

import sys
import logging

from urlparse import urlparse, urljoin

try:
    import requests
    logging.getLogger("requests").setLevel(logging.WARNING)
except ImportError:
    requests = None

try:
    import redis
except ImportError:
    redis = None


class BrokerBase(object):
    def __init__(self, broker_url, *args, **kwargs):
        purl = urlparse(broker_url)
        self.host = purl.hostname
        self.port = purl.port
        self.vhost = purl.path[1:]
        self.username = purl.username
        self.password = purl.password

    def queues(self, names):
        raise NotImplementedError


class RabbitMQ(BrokerBase):
    def __init__(self, broker_url, broker_api_url):
        super(RabbitMQ, self).__init__(broker_url)
        self._broker_api_url = broker_api_url

        if not requests:
            raise ImportError('requests library is required')

    def queues(self, names):
        if not self._broker_api_url.endswith('/'):
            self._broker_api_url += '/'
        url = urljoin(self._broker_api_url, 'queues/' + self.vhost)
        api_url = urlparse(self._broker_api_url)
        username = api_url.username or self.username
        password = api_url.password or self.password
        auth = requests.auth.HTTPBasicAuth(username, password)
        r = requests.get(url, auth=auth)

        if r.status_code == 200:
            info = r.json()
            return filter(lambda x: x['name'] in names, info)
        else:
            r.raise_for_status()


class Redis(BrokerBase):
    def __init__(self, broker_url, *args, **kwargs):
        super(Redis, self).__init__(broker_url)
        host = self.host or '127.0.0.1'
        port = self.port or 6379
        db = self.vhost or 0

        if not redis:
            raise ImportError('redis library is required')

        self._redis = redis.Redis(host=host, port=port,
                                  db=db, password=self.password)

    def queues(self, names):
        return map(lambda x: dict(name=x, messages=self._redis.llen(x)),
                   names)


class Broker(object):
    def __new__(cls, broker_url, *args, **kwargs):
        scheme = urlparse(broker_url).scheme
        if scheme == 'amqp':
            return RabbitMQ(broker_url, *args, **kwargs)
        elif scheme == 'redis':
            return Redis(broker_url, *args, **kwargs)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    broker_url = sys.argv[1] if len(sys.argv) > 1 else 'amqp://'
    queue_name = sys.argv[2] if len(sys.argv) > 2 else 'celery'
    if len(sys.argv) > 3:
        broker_api_url = sys.argv[3]
    else:
        broker_api_url = 'http://guest:guest@localhost:55672/api/'

    broker = Broker(broker_url, broker_api_url=broker_api_url)
    print(broker.queues([queue_name]))
