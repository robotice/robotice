#!/usr/bin/python
import os

import logging
import statsd
import redis
import socket

from yaml import load, dump, safe_dump

from robotice.utils.celery import init_sentry
from redis_collections import Dict, List

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
            full_conf_path = "%s/{0}.yml" % self.conf_dir
            config_file = open(full_conf_path.format(name), "r")
            yaml_file = load(config_file)

            setattr(self, "".join([prefix, name]), yaml_file)

        except Exception, e:
            raise e

        return True

    def setup_app(self, worker):
        """main method which init all settings for specific role
        """

        if not isinstance(worker, basestring):
            raise Exception("Only string is allowed for worker.")

        self.worker = worker

        config_file = open(
            "".join([self.worker_dir, "/config_%s.yml" % worker]), "r")
        self.config = load(config_file)

        if "dsn" in self.config:
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

    def uuid(self, host=None, worker=None, device=None):
        """return uuid for host and role
        """
        if not host:
            host = self.hostname
        if not worker:
            worker = self.worker

        if device:
            key = ".".join([host, device])

        key = ".".join([host, worker])

        return key

    @property
    def devices(self):
        return self._devices

    def save_sensor(self, name, sensor, only_db=False):
        """method save sensor into two keys
        host.sensors.metric.name as dict
        and update host.sensors list
        """

        # set host.sensors.metric.name as dict

        if not sensor.get("metric", None) \
            or not sensor.get("name", None):
            raise Exception("missing sensor name or metric %s" % sensor)

        key = ".".join([
            name, 
            sensor.get("type"),
            sensor.get("metric"),
            sensor.get("name")
        ])

        saved_as_dict = self.update_or_create(sensor, key)

        # for load from file
        if not only_db:
            result = self.dump_to_file(name, dict(saved_as_dict), sensor.get("type"))

        # update host.sensors list
        key = ".".join([name, "sensors"])

        saved_as_list = self.update_or_create([sensor], key)

        return saved_as_list

    def save_plan(self, name, plan, key="sensors", only_db=False):
        """method save sensor into two keys
        host.sensors.metric.name as dict
        and update host.sensors list
        """
        result = self.dump_to_file(name, plan, key, "plans")
        return result

    def save_system(self, name, system, key="sensors", only_db=False):
        """method save sensor into two keys
        host.sensors.metric.name as dict
        and update host.sensors list
        """
        result = self.dump_to_file(name, system, key, "systems")
        return result

    def save_actuator(self, actuator, host):
        key = self.uuid(host, "actuators")

        if not actuator.get("system_plan", None) \
            or not actuator.get("device", None):
            raise Exception(
                "missing actuator device or system_plan %s" % actuator)

        key = ".".join(
            [host,
            "actuators",
            actuator.get("system_plan"),
            actuator.get("device")])

        saved_as_dict = self.update_or_create(actuator, key)

        # update host.sensors list
        key = ".".join([host, "actuators"])

        saved_as_list = self.update_or_create([actuator], key)

        return saved_as_list

    def save_meta(self, name, metadata, attr="systems"):
        """saves metadata
        """

        items = getattr(self, attr) # copy local devices

        if name in items:
            # update
            obj = items[name]
            for key, value in metadata.iteritems():
                if key in obj:
                    obj[key] = value
            items[name] = obj
        else:
            # create
            if not "actuators" in metadata \
            or not "sensors" in metadata:
                # init
                metadata["actuators"] = {}
                metadata["sensors"] = {}
            items[name] = metadata

        # write to file

        full_conf_path = "%s/%s.yml" % (self.conf_dir, attr)

        self.dump_to_file_and_set(
            full_conf_path,
            items,
            attr)

        return True

    def dump_to_file_and_set(self, path, items, name):
        """helper
        TODO: move into utils
        """
        try:
            with open(path, 'w') as yaml_file:
                safe_dump(items, yaml_file, default_flow_style=False)

            # set new items
            setattr(self, "_%s" % str(name), items)
        except Exception, e:
            # cannot write to disk
            raise e

        return True

    def delete(self, obj, host, key="sensors", attr="devices"):
        """delete object from file
        
        attr = plans, systems, devices

        .. code-block:: yaml
            obj = { id: 10 } or name / device
        """
        deleted = True
        items = getattr(self, attr) # copy local devices

        for id, system in getattr(self, attr).iteritems():
            if id in host:
                _dict = system.get(key)
                
                name = obj.pop("id", None)
                
                if not name:
                    name = obj.get("name", obj.get("device", None))
                
                if not name:
                    raise Exception("missing id, name or device %s" % obj)

                # actuator or sensor
                if name in _dict:
                    _dict.pop(name)
                    deleted = False # switch to update
                elif name in items:
                    # host
                    items.pop(name)
                    deleted = False # switch to update


        if deleted:
            # write to file
            full_conf_path = "%s/%s.yml" % (self.conf_dir, attr)

            self.dump_to_file_and_set(
                full_conf_path,
                items,
                attr)

        return True


    def dump_to_file(self, name, data, key="sensors", attr="devices"):
        """dump new sensor or actuator to file
        
        attr = plans, systems, devices

        .. code-block:: yaml
            hostname:
              sensors:
                id:
                  type: type
                  name: name
                  port: port
              actuators:
                id:
                  port: port
        """
        created = True
        items = getattr(self, attr) # copy local devices

        for id, system in getattr(self, attr).iteritems():
            if id in name:
                _dict = system.get(key)
                
                name = obj.pop("id", None)
                
                if not name:
                    name = obj.get("name", obj.get("device", None))
                
                if not name:
                    raise Exception("missing id, name or device %s" % obj)

                _dict[name] = obj
                items[id][key] = _dict

                created = False # switch to update

        if created:
            self.save_meta(
                name,
                data,
                attr=attr
                )
        else:
            # write to file
            full_conf_path = "%s/%s.yml" % (self.conf_dir, attr)

            self.dump_to_file_and_set(
                full_conf_path,
                items,
                attr)

        return True

    def get_sensors(self, host=None):
        key = self.uuid(host, "sensors")

        sensors = List([], key=key, redis=self.database)

        if len(sensors) == 0:
            sensors = self.load_sensors()

        return list(sensors)

    @property
    def sensors(self, host=None):
        """return list of sensors by key hostname.sensors
        default to self.hostname
        if sensors is empty method call load_sensors from file
        """

        key = self.uuid(self.hostname, "sensors")

        sensors = List([], key=key, redis=self.database)

        if len(sensors) == 0:
            # load all sensors
            # returns sensors for all hosts !!
            sensors = self.load_sensors()

        return list(sensors)

    @property
    def actuators(self):
        """return list of sensors by key hostname.sensors
        default to self.hostname
        if sensors is empty method call load_sensors from file
        """

        key = self.uuid(self.hostname, "actuators")

        actuators = List([], key=key, redis=self.database)

        if len(actuators) == 0:
            actuators = self.load_actuators()

        return list(actuators)

    def load_actuators(self):
        """return actuators for all systems, but add `system_name` variable"""

        actuators = []
        for name, system in self.systems.iteritems():
            for uuid, actuator in system.get('actuators').iteritems():
                
                if not "device" in actuator:
                    actuator['device'] = uuid
                
                actuator['system_name'] = system.get('name')
                actuator['system_plan'] = system.get('plan')
                actuators.append(actuator)
                self.save_actuator(actuator, host=self.hostname)  # save to db

        LOG.debug(actuators)

        return actuators

    def update_or_create(self, instance, key):
        """method accept list or dict
        both save into redis as Dict or List
        if instance is a list method automaticaly update list in redis
        """

        created = True

        if isinstance(instance, dict):
            # save dictionary
            try:
                saved = Dict(instance, key=key, redis=self.database)
            except Exception, e:
                raise e

            return saved

        # update list especially sensors or actuators collection
        if isinstance(instance, list):
            try:
                devices = List([], key=key, redis=self.database)
            except Exception, e:
                raise e

            update = []

            for device in devices:
                if device.get("id") == instance.get("id"):
                    update.append(instance)
                    created = False
                else:
                    update.append(device)

            if created:
                update.append(instance)

            r = List(update, key=key, redis=self.database)

            return list(r)

        return False

    @property
    def systems(self):
        return self._systems

    @property
    def plans(self):
        return self._plans

    def load_sensors(self, host=None, worker=None):
        """method load and save sensors from self._devices file
        """

        sensors = []

        for name, host in self.devices.iteritems():

            for name, sensor in host.get('sensors').iteritems():

                if not "name" in sensor:
                    sensor["name"] = name

                sensor['os_family'] = self.config.get("os_family")
                sensor['cpu_arch'] = self.config.get("cpu_arch")
                sensor['hostname'] = self.hostname
                sensors.append(sensor)
                self.save_sensor(sensor, host=self.hostname, only_db=True)  # save to db
            
        LOG.debug(sensors)

        return sensors

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
    def get_system_plans(self):
        """return array of tuples [(system, plan),]"""

        results = []
        for name, system in self.systems.iteritems():
            system["name"] = name  # hotfix
            for name, plan in self.plans.iteritems():
                plan["name"] = name # hotfix
                if name == system.get("plan"):
                    results.append((system, plan),)
        return results

    def get_plan(self, device_name, device_metric=None):
        """return tuple (system, plan)
        """

        result = (None, None)

        for name, system in self.systems.iteritems():

            system["name"] = name  # hotfix

            for uuid, sensor in system.get('sensors').iteritems():
                sensor["device"] = uuid # hotfix
                if device_metric \
                    and "metric" in sensor:
                    if (sensor.get('device', None) == device_name
                       or sensor.get('name', None) == device_name) \
                        and sensor.get("metric") == device_metric:
                        result = system, sensor.get('plan')
                else:
                    if sensor.get('name') == device_name:
                        result = system, sensor.get('plan')
        return result

    def get_actuator_device(self, device_name):
        """return actuator from host devices"""

        for name, host in self.devices.iteritems():
            for uuid, device in host.get('actuators').iteritems():
                device["device"] = uuid # hotfix
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
    """A singleton implementation of Settings such that all dealings
    with settings get the same instance no matter what. There can be only one.
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
