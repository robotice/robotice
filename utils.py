#!/usr/bin/python

import logging
from yaml import load
import statsd
import redis

log = logging.getLogger("robotice.utils")

class Settings(object):
    name = None
    system = None
    broker = None
    database = None
    metering = None
    sensors = None
    actuators = None

    def __init__(self):

        config_file = open("/srv/robotice/config.yml", "r")
        config = load(config_file)

        self.name = config.get('name').replace('.', '_')
        self.system = config.get('system')
        self.metering = config.get('metering')
        self.database = config.get('database')
        self.broker = config.get('broker')
        self.sensors = config.get('sensors')
        self.actuators = config.get('actuators')

    @property
    def get_database(self):
        return redis.Redis(host=self.database.get('host'), port=self.database.get('port'), db=0)

    @property
    def get_metering(self):
        statsd_connection = statsd.Connection(
            host=self.metering.get('host'),
            port=self.metering.get('port'),
            sample_rate=self.metering.get('sample_rate'),
            disabled = False
        )
        return statsd.Gauge('%s.%s' % (self.system, self.name), statsd_connection)

def setup_app():
    app = Settings()
    return app
