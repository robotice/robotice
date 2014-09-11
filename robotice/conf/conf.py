#!/usr/bin/python
import os

import logging
import statsd
import redis
import socket

from yaml import load

from robotice.utils.celery import init_sentry

LOG = logging.getLogger(__name__)

class Settings(object):

    """**Main object which contains all infromation about systems**

    Args:
       worker (str):  The role name to use.
       conf_dir (str):  path to root of config.
       worker_dir (str):  path to root of workers config.

    you can change config PATH

    if you set system variable R_CONFIG_DIR and R_worker_dir

    in directory `R_CONFIG_DIR` is expected devices.yml, systems.yml, plans.yml
    in directory `R_worker_dir` is expected worker_monitos.yml etc.

    """

    def load_conf(self, name):
        """encapsulation logic for load yaml

        Args:
           name (str):  The role name to use.

        Returns:
           boolean. The return code::

              True -- Success!

        Raises:
           Exception, KeyError
        """

        try:
            full_conf_path = "%s/{0}.yml" % self.conf_dir
            config_file = open(full_conf_path.format(name), "r")
            yaml_file = load(config_file)
            if yaml_file.get(name, None):
                setattr(self, name, yaml_file[name])
            else:
                raise Exception("file missing main key %s" % name)
        except Exception, e:
            raise Exception(
                "File devices could not load, original exception: %s" % e)

        return True

    def setup_app(self, worker):
        """main method which init all settings for specific role
        """

        if not isinstance(worker, basestring):
            raise Exception("Only string is allowed for worker.")

        self.worker = worker

        config_file = open("".join([self.worker_dir, "/config_%s.yml" % worker ]), "r")
        self.config = load(config_file)

        if self.config.has_key("dsn"):
            init_sentry(self.config.get("dsn"))

        if worker == "reasoner":

            self.load_conf("devices")

            self.load_conf("plans")

            self.load_conf("systems")

    def __init__(self, worker=None, conf_dir="/srv/robotice/config",
                 worker_dir="/srv/robotice"):

        if worker:
            self.setup_app(worker)

        self.conf_dir = os.getenv("R_CONFIG_DIR", conf_dir)
        self.worker_dir = os.getenv("R_WORKER_DIR", worker_dir)

        LOG.debug("Main configuration PATH: %s" % self.conf_dir)
        LOG.debug("Worker PATH: %s" % self.worker_dir)

    def uuid(self, host=None, worker=None):
        """return uuid for host and role
        """
        if not host:
            host = self.hostname
        if not worker:
            worker = self.worker

        key = ".".join([host, worker])
        
        return key

    def set_system(self, system, host=None, worker=None):
        """set system direcly into database and file backend
        """

        key = self.uuid(host, worker)
        
        if system:

            try:
                result = self.database.set(key, system)
                if not result:
                    raise Exception(result)
                system = self.database.get(key)
            except Exception, e:
                raise e

        return system
        
    def get_system(self, host=None, worker=None):
        """return plan for host and role from db or file
        """
        key = self.uuid(host, worker)
        _system = self.database.get(key)

        if not _system:
            # sync to db
            try:
                _system = {}
                _system["actuators"] = self.actuators
                _system["sensors"] = self.sensors
                _system["plans"] = self.get_system_plans
                result = self.database.set(key, _system)
                if not result:
                    raise Exception(result)
            except Exception, e:
                raise e

        return _system

    @property
    def sensors(self):

        sensors = []

        for host in self.devices:
            # operator in support match in two forms `ubuntu1` or
            # `ubuntu1.domain.com`
            if host.get('host') in self.hostname:
                for sensor in host.get('sensors'):
                    sensor['os_family'] = self.config.get("os_family")
                    sensor['cpu_arch'] = self.config.get("cpu_arch")
                    sensor['hostname'] = self.hostname
                    sensors.append(sensor)

        LOG.debug(sensors)

        return sensors

    @property
    def actuators(self):
        """return actuators for all systems, but add `system_name` variable"""
        actuators = []
        for system in self.systems:
            for actuator in system.get('actuators'):
                actuator['system_name'] = system.get('name')
                actuator['system_plan'] = system.get('plan')
                actuators.append(actuator)

        LOG.debug(actuators)

        return actuators

    @property
    def get_system_plans(self):
        """return array of tuples [(system, plan),]"""
        
        results = []
        for system in self.systems:
            for plan in self.plans:
                if plan.get("name") == system.get("plan"):
                    results.append((system, plan),)
        return results

    def get_plan(self, device_name, device_metric=None):
        """return tuple (system, plan)
        """

        result = (None, None)

        for system in self.systems:
            for sensor in system.get('sensors'):
                
                if device_metric \
                and sensor.has_key("metric"):
                    if (sensor.get('device', None) == device_name \
                    or sensor.get('name', None) == device_name) \
                    and sensor.get("metric") == device_metric:
                        result = system, sensor.get('plan')
                else:
                    if sensor.get('name') == device_name:
                        result = system, sensor.get('plan')                        
        return result

    def get_actuator_device(self, device_name):
        """return actuator from host devices"""

        for host in self.devices:
            for device in host.get('actuators'):
                if device_name == device.get('name'):
                    return device
        return None

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

        _redis = redis.Redis(
            host=self.config.get('database').get('host'),
            port=self.config.get('database').get('port'),
            db=self.config.get('database').get('number', 0))

        LOG.debug("Inicialized database connection %s " % _redis)
        
        return _redis

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