#!/usr/bin/python

import logging
from yaml import load
import statsd
import redis
import socket

from grains import grains

LOG = logging.getLogger(__name__)


class Settings(object):

    config = None
    devices = None
    systems = None
    plans = None

    def setup_app(self, worker):
        config_file = open("/srv/robotice/config_%s.yml" % worker, "r")
        self.config = load(config_file)

        if worker == "reasoner":

            device_config_file = open("/srv/robotice/config/devices.yml", "r")
            self.devices = load(device_config_file)['devices']

            plan_config_file = open("/srv/robotice/config/plans.yml", "r")
            self.plans = load(plan_config_file)['plans']

            system_config_file = open("/srv/robotice/config/systems.yml", "r")
            self.systems = load(system_config_file)['systems']

    def __init__(self, worker=None):

        if worker:
            self.setup_app(worker)

    @property
    def sensors(self):
        
        if not getattr(self, "sensors", None):
            for host in self.devices:
                if host.get('host') == self.hostname:
                    for sensor in host.get('sensors'):
                        sensor['os_family'] = self.grains.os_family
                        sensor['cpu_arch'] = self.grains.cpu_arch
                        sensor['hostname'] = self.hostname
                        sensors.append(sensor)
        return sensors

    @property
    def get_system_plans(self):
        """vraci pole tuplu [(system, plan),]"""
        results = []
        for system in self.systems:
            for plan in self.plans:
                if plan.get("name") == system.get("plan"):
                    results.append((system, plan),)
        return results

    @property
    def hostname(self):
        return socket.getfqdn()

    @property
    def broker(self):
        """broker in string format
        redis://localhost:6379/9
        """
        return self.config.get('broker')

    @property
    def database(self):
        """database connection
        now is supported only redis
        """
        redis = getattr(self, "redis", None)
        if not redis:
            self.redis = redis.Redis(
                host=self.config.get('database').get('host'),
                port=self.config.get('database').get('port'),
                db=self.config.get('database').get('number', 0))
        return self.redis

    @property
    def metering_prefix(self):
        #return '%s_%s.%s' % (self.config.get('system_name'), self.config.get('environment'), self.hostname.replace('.', '_'))
        return 'robotice'

    @property
    def metering(self):
        meter = getattr(self, "meter", None)
        if not meter:
            statsd_connection = statsd.Connection(
                host=self.config.get('metering').get('host'),
                port=self.config.get('metering').get('port'),
                sample_rate=self.config.get('metering').get('sample_rate'),
                disabled=False
            )
            self.meter = statsd.Gauge(self.metering_prefix, statsd_connection)
        return meter

    @property
    def grains(self):
        return grains


class RoboticeSettings(Settings):
    """A singleton implementation of Settings such that all dealings with settings
    get the same instance no matter what. There can be only one.
    you can use RoboticeSettings('reasoner') or setup_app declared below
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
        return cls._instance


settings = RoboticeSettings() # one true Settings


def setup_app(worker):
    """dealing with global singleton and load configs
    """
    global settings

    settings.setup_app(worker)

    return settings