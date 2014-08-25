#!/usr/bin/python

import logging
from yaml import load
import statsd
import redis
import socket

log = logging.getLogger("robotice.conf")


def import_module(name):
    mod = __import__(name)
    components = name.split('.')

    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod

class Settings(object):

    config = None
    devices = None
    systems = None
    plans = None

    def __init__(self, worker):

        config_file = open("/srv/robotice/config_%s.yml" % worker, "r")
        self.config = load(config_file)

        device_config_file = open("/srv/robotice/config/devices.yml", "r")
        self.devices = load(device_config_file)['devices']

        plan_config_file = open("/srv/robotice/config/plans.yml", "r")
        self.plans = load(plan_config_file)['plans']

        system_config_file = open("/srv/robotice/config/systems.yml", "r")
        self.systems = load(system_config_file)['systems']

    @property
    def sensors(self):
        sensors = []
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
    def grains(self):
        grains = Grains()
        return grains

    @property
    def hostname(self):
        return socket.getfqdn()

    @property
    def broker(self):
        return self.config.get('broker')

    @property
    def database(self):
        return redis.Redis(host=self.config.get('database').get('host'), port=self.config.get('database').get('port'), db=self.config.get('database').get('number', 0))

    @property
    def metering_prefix(self):
        #return '%s_%s.%s' % (self.config.get('system_name'), self.config.get('environment'), self.hostname.replace('.', '_'))
        return 'robotice'

    @property
    def metering(self):
        statsd_connection = statsd.Connection(
            host=self.config.get('metering').get('host'),
            port=self.config.get('metering').get('port'),
            sample_rate=self.config.get('metering').get('sample_rate'),
            disabled=False
        )
        return statsd.Gauge(self.metering_prefix, statsd_connection)

    @property
    def grains(self):
        return get_grains()


def setup_app(worker):
    return Settings(worker)

class Grains(object):

    hostname = None
    os_family = None
    cpu_arch = None
    
    def __init__(self):

        grains_file = open("/srv/robotice/grains.yml", "r")
        grains = load(grains_file)['grains']

        self.hostname = grains['hostname']
        self.os_family = grains['os_family']
        self.cpu_arch = grains['cpu_arch']

def get_grains():
    grains = Grains()
    return grains
