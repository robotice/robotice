#!/usr/bin/python

import logging
from yaml import load
import statsd
import redis
import socket

log = logging.getLogger("robotice.utils")

class Settings(object):

    config = None
    
    def __init__(self):

        config_file = open("/srv/robotice/config.yml", "r")
        self.config = load(config_file)

    @property
    def plans(self):
        plans = []
        for host in self.config.get('system'):
            if host.get('name') == self.hostname:
                for plan in host.get('plans'):
                    plans.append({
                        "start": plan.get('start'),
                        "plan": load(open("/srv/robotice/service/plans/%s" % plan.get('type'))),
                        "name": plan.get('name')
                    })
        return plans

    @property
    def sensors(self):
        sensors = []
        for host in self.config.get('system'):
            if host.get('name') == self.hostname:
                for sensor in host.get('sensors'):
                    sensor['os_family'] = host.get('os_family')
                    sensor['cpu_arch'] = host.get('cpu_arch')
                    sensor['hostname'] = self.hostname
                    sensors.append(sensor)
        return sensors

    @property
    def hostname(self):
        return socket.getfqdn()

    @property
    def broker(self):
        return self.config.get('broker')

    @property
    def database(self):
        return redis.Redis(host=self.config.get('database').get('host'), port=self.config.get('database').get('port'), db=0)

    @property
    def metering_prefix(self):
        return '%s_%s.%s' % (self.config.get('system_name'), self.config.get('environment'), self.hostname.replace('.', '_'))

    @property
    def metering(self):
        statsd_connection = statsd.Connection(
            host=self.config.get('metering').get('host'),
            port=self.config.get('metering').get('port'),
            sample_rate=self.config.get('metering').get('sample_rate'),
            disabled = False
        )
        return statsd.Gauge(self.metering_prefix, statsd_connection)

def setup_app():
    app = Settings()
    return app
