#!/usr/bin/python

import logging
from yaml import load
import statsd
import redis

log = logging.getLogger("robotice.utils")

class Settings(object):
    broker = None
    database = None
    metering = None
    sensors = None
    actuators = None

    def __init__(self):

        config_file = open("/srv/robotice/config.yml", "r")
        config = load(config_file)

        statsd_connection = statsd.Connection(
            host=config.get('metering').get('host'),
            port=config.get('metering').get('port'),
            sample_rate=config.get('metering').get('sample_rate'),
            disabled = False
        )
        self.metering = statsd.Gauge('%s.%s' % (config.get('system'), config.get('name').replace('.', '_')), statsd_connection)
        self.database = redis.Redis(host=config.get('database').get('host'), port=config.get('database').get('port'), db=0)
        self.broker = config.get('broker')
        self.sensors = config.get('sensors')
        self.actuators = config.get('actuators')

def setup_app():
    app = Settings()
    return app

