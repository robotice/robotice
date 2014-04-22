#!/usr/bin/python

import logging
from yaml import load
import statsd
import redis
import socket

from models import Plan, Device, System, Sensor, Config

from pymongo import connection
from blitzdb.backends.mongo import Backend as MongoBackend
from blitzdb import FileBackend

log = logging.getLogger("robotice.utils")

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
    def mongo_connection(self):
        return connection(self.config.get('database_mongo').get('host'), self.config.get('database_mongo').get('port'))

    @property
    def mongodb_backend(self, db_name=self.get_grains.hostname):
        """http://api.mongodb.org/python/2.7rc0/tutorial.html
        return mongodb backend
        http://blitz-db.readthedocs.org/en/latest/backends/mongo.html
        """
        db = self.mongo_connection[db_name]
        return MongoBackend(db)
    
    @property
    def file_backend(self, db="/srv/robotice/database"):
        """
        db with path
        """
        return FileBackend(db)

    def load_model_from_mongo(self, worker):
        """
        loadne model z mognodb a ulozi je na disk do souborove db
        pokud bude existovat tak by to mel syncnout v pripade failu vytvorit novou db2
        """
        return True

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
