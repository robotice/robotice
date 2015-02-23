#!/usr/bin/python

from __future__ import absolute_import

import os

import logging
import statsd
import redis
import socket
import pickle
import anyconfig

from yaml import load, dump, safe_dump

from kombu.utils import symbol_by_name

LOG = logging.getLogger(__name__)

from robotice.utils import deprecated
from robotice.utils import PickledRedis
from robotice.utils import norecursion
from robotice.utils import dict_merge
from robotice.utils.celery import init_sentry

from robotice.conf.managers import actions
from robotice.conf.managers import plans
from robotice.conf.managers import systems
from robotice.conf.managers import devices

BACKEND_ALIASES = {
    'cache': 'robotice.utils.backends.cache:CacheBackend',
    'redis': 'robotice.utils.backends.redis:RedisBackend',
    'mongodb': 'robotice.utils.backends.mongodb:MongoBackend',
}

DEFAULT_COMPARATOR_ALIASES = {
    'simple': 'robotice.reasoner.comparators.base:BaseComparator',
#    'fuzzy': 'robotice.utils.extensions.comparators.fuzzy:FuzzyComparator',
}

class Settings(object):
    """**Main object which contains all infromation about systems**

    Args:
       worker (str):  The role name to use.
       conf_dir (str):  path to root of config.
       worker_dir (str):  path to root of workers config.

    you can change config PATH

    if you set system variable R_CONFIG_DIR and R_worker_dir

    in directory `R_CONFIG_DIR` is expected devices.yml, systems.yml, plans.yml
    in directory `R_WORKER_DIR` is expected worker_monitos.yml etc.

    R_DRIVERS_DIR is drivers directory and default is /srv/robotice/drivers

    """

    def load_conf(self, name, prefix="_"):
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
            full_conf_path = "%s/{0}.yml" % self.CONF_DIR
            config_file = open(full_conf_path.format(name), "r")
            yaml_file = load(config_file)

            setattr(self, "".join([prefix, name]), yaml_file)

        except Exception, e:
            raise e

        return True

    WORKER_DIR = os.getenv("R_WORKER_DIR", "/srv/robotice")
    CONF_DIR = os.getenv("R_CONFIG_DIR", "/srv/robotice/config")
    DRIVERS_DIR = "/srv/robotice/drivers"

    db_backend_name = "redis" # TODO propagation from config

    @property
    def comparators(self):
        """return configured comparators
        default is simple comparator
        """
        return self.config.get("comparators", None) or DEFAULT_COMPARATOR_ALIASES


    @property
    def config(self):
        config_file = open(
            "".join([self.WORKER_DIR, "/config_%s.yml" % self.worker]), "r")
        self._config = load(config_file)
        return self._config

    def setup_app(self, worker):
        """main method which init all settings for specific role
        """

        self.setup_sys_vars() # inicialize system variables

        if not isinstance(worker, basestring):
            raise Exception("Only string is allowed for worker.")

        self.worker = worker

        if "dsn" in self.config:
            init_sentry(self.config.get("dsn"))

    def setup_sys_vars(self):

        os.environ.setdefault("R_WORKER_DIR", self.WORKER_DIR)
        os.environ.setdefault("R_CONFIG_DIR", self.CONF_DIR)
        os.environ.setdefault("R_DRIVERS_DIR", self.DRIVERS_DIR)

    def __init__(self, worker=None):

        if worker:
            self.setup_app(worker)

        LOG.debug("Main configuration PATH: %s" % self.CONF_DIR)
        LOG.debug("Worker PATH: %s" % self.WORKER_DIR)

        # these managers provide list, get, set, delete
        self.actions = actions
        self.plans = plans
        self.systems = systems
        self.devices = devices

    @property
    def sensors(self):
        """return list of sensors by key hostname.sensors
        default to self.hostname
        if sensors is empty method call load_sensors from file
        """
        key = ":".join([
            self.hostname,
            "sensors"
            ])

        # ugly hack
        # maybe exist better way to map key as name
        sensors = []
        for key, sensor in self.devices.get(key).iteritems():
            sensor["name"] = key
            sensors.append(sensor)

        return sensors

    def __get_plan(self, actuator):
        key = ":".join([
            str(actuator["system_plan"]),
            "actuators",
            str(actuator["plan"])])

        plan = self.plans.get(key)
        LOG.debug(key)
        LOG.debug(plan)
        return plan

    @property
    def actuators(self):
        """return actuators for all systems, with added `system_name` variable"""
        
        actuators = []

        systems = anyconfig.load([self.systems.config_path, self.devices.config_path], merge=anyconfig.MS_DICTS)

        for system_name, system in self.systems.list().iteritems():
            for uuid, actuator in system.get('actuators').iteritems():

                actuator["id"] = uuid
                actuator['system_name'] = system_name
                actuator['system_plan'] = system.get('plan')

                plan = self.__get_plan(actuator)
                if not plan:
                    LOG.error("missing plan for %s object: %s" % (uuid,actuator))
                    continue
                actuator["plan_full"] = plan
                actuator["plan_name"] = plan["name"]
                actuators.append(actuator)

        LOG.debug(actuators)

        return actuators

    @property
    def get_system_plans(self):
        """return array of tuples [(system, plan),]"""

        results = []
        for hostname, system in self.systems.list().iteritems():
            system["name"] = hostname
            for plan_name, plan in self.plans.list().iteritems():
                plan["name"] = plan_name # hotfix
                if plan_name == system.get("plan"):
                    results.append((system, plan),)
        return results

    def get_plan(self, device_name, device_metric=None):
        """return tuple (system, plan)
        """

        def _get_plan(conf, sensor):
            key = ":".join([
                sensor["system_plan"],
                "sensors",
                str(sensor["plan"])])

            plan = self.plans.get(key)

            if not plan:
                LOG.error("plan for %s not found" % sensor)
            return plan

        result = (None, None)

        for name, system in self.systems.list().iteritems():

            system["name"] = name
            devices = self.systems.get("%s:sensors" % name)

            for uuid, sensor in devices.iteritems():

                sensor["system_plan"] = system["plan"]
                LOG.debug(sensor)

                if device_metric \
                    and "metric" in sensor:
                    if (sensor.get('device', None) == device_name
                       or sensor.get('name', None) == device_name) \
                        and sensor.get("metric") == device_metric:
                        result = system, _get_plan(self, sensor)
                else:
                    if sensor.get('name') == device_name:
                        result = system, _get_plan(self, sensor)
        if None in result:
            LOG.error("device_name: %s & device_metric: %s " % (device_name, device_metric))
        return result

    def get_actuator_device(self, actuator):
        """return actuator from host devices"""

        for name, host in self.devices.list().iteritems():
            for uuid, device in host.get('actuators').iteritems():
                if ("actuator" in actuator and actuator["actuator"] == uuid) \
                or ("device" in actuator and actuator["device"] == uuid) \
                or ("name" in actuator and (actuator["name"] == uuid \
                    or actuator["name"] == device.get("name"))):
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
    def db(self):
        """only alias for db
        """
        try:
            self.db_backend_cls = symbol_by_name(BACKEND_ALIASES[self.db_backend_name])
        except Exception, e:
            raise e

        _client = self.db_backend_cls(
            host=self.config.get('database').get('host'),
            port=self.config.get('database').get('port'),
            db=self.config.get('database').get('number', 0))

        LOG.debug("Inicialized database connection %s " % _client)

        return _client

    @property
    def database(self):
        """database connection
        now is supported only redis

        TODO: database is too long, mark this as deprecated
        """
        
        return self.db


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
    """
    you can use RoboticeSettings('reasoner') or setup_app declared below
    """
    pass

settings = RoboticeSettings()


def setup_app(worker):
    """dealing with global setting and load configs
    easiest way how you get settings instance is RoboticeSettings('reasoner')
    """
    global settings

    settings.setup_app(worker)

    return settings
