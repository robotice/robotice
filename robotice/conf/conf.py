#!/usr/bin/python

import logging
import statsd
import redis
import socket

from yaml import load
from grains import grains

LOG = logging.getLogger(__name__)


class Settings(object):

    """Main object which contains all infromation about systems
    """

    def load_conf(self, _type):
        """encapsulation logic for load yaml
        """
        try:
            full_conf_path = "%s{0}.yml" % self.conf_dir
            config_file = open(full_conf_path.format(_type), "r")
            yaml_file = load(config_file)
            if yaml_file.get(_type, None):
                setattr(self, _type, yaml_file[_type])
            else:
                raise Exception("file missing main key %s" % _type)
        except Exception, e:
            raise Exception(
                "File devices could not load, original exception: %s" % e)

    def setup_app(self, worker):
        """main method which init all settings for specific role
        """

        if not isinstance(worker, basestring):
            raise Exception("Only string is allowed for worker.")

        self.worker = worker

        config_file = open("/srv/robotice/config_%s.yml" % worker, "r")
        self.config = load(config_file)

        if worker == "reasoner":

            self.load_conf("devices")

            self.load_conf("plans")

            self.load_conf("systems")

    def __init__(self, worker=None, conf_dir="/srv/robotice/config/", 
        workers_dir="/srv/robotice/service"):

        if worker:
            self.setup_app(worker)

        self.conf_dir = conf_dir
        self.workers_dir = workers_dir

    @property
    def sensors(self):

        sensors = []

        if not getattr(self, "_sensors", None):
            for host in self.devices:
                # operator in support match in two forms `ubuntu1` or
                # `ubuntu1.domain.com`
                if host.get('host') in self.hostname:
                    for sensor in host.get('sensors'):
                        sensor['os_family'] = self.grains.os_family
                        sensor['cpu_arch'] = self.grains.cpu_arch
                        sensor['hostname'] = self.hostname
                        sensors.append(sensor)
            self._sensors = sensors
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
        _redis = getattr(self, "redis", None)
        if _redis is None:
            self.redis = redis.Redis(
                host=self.config.get('database').get('host'),
                port=self.config.get('database').get('port'),
                db=self.config.get('database').get('number', 0))
        return self.redis

    @property
    def metering(self):
        """method create instance of statsd client
        method expected metering settings in worker config file
        metering:
          host: localhost is default
          port: 8125 is default
          sample_rate: 1 is default
          prefix: robotice is default
        """
        meter = getattr(self, "meter", None)
        if not meter:
            statsd_connection = statsd.Connection(
                host=self.config.get('metering').get('host', '127.0.0.1'),
                port=self.config.get('metering').get('port', 8125),
                sample_rate=self.config.get('metering').get('sample_rate', 1),
                disabled=False
            )
            self.meter = statsd.Gauge(
                self.config.get('metering').get('prefix', 'robotice'),
                statsd_connection)
        return self.meter

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


settings = RoboticeSettings()  # one true Settings


def setup_app(worker):
    """dealing with global singleton and load configs
    easiest way how you get settings instance is RoboticeSettings('reasoner')
    """
    global settings

    settings.setup_app(worker)

    return settings
