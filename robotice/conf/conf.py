#!/usr/bin/python
import os

import logging
import statsd
import redis
import socket

from yaml import load, dump, safe_dump

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

    @property
    def config(self):
        config_file = open(
            "".join([self.WORKER_DIR, "/config_%s.yml" % self.worker]), "r")
        self._config = load(config_file)
        return self._config

    def setup_app(self, worker):
        """main method which init all settings for specific role
        """

        if not isinstance(worker, basestring):
            raise Exception("Only string is allowed for worker.")

        self.worker = worker

        if "dsn" in self.config:
            init_sentry(self.config.get("dsn"))

        if worker == "reasoner":

            self.load_conf("devices")

            self.load_conf("plans")

            self.load_conf("systems")

    def __init__(self, worker=None):

        if worker:
            self.setup_app(worker)

        LOG.debug("Main configuration PATH: %s" % self.CONF_DIR)
        LOG.debug("Worker PATH: %s" % self.WORKER_DIR)

    def uuid(self, host=None, worker=None, device=None):
        """return uuid for host and role
        """
        if not host:
            host = self.hostname
        if not worker:
            worker = self.worker

        if device:
            key = ".".join([str(host), device])

        key = ".".join([str(host), worker])

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

        if not sensor.get("metric") \
            or not sensor.get("name"):
            raise Exception("missing sensor name or metric %s" % sensor)

        # fix get by string number
        sensor_name = sensor.get("name")
        if isinstance(sensor_name, basestring) and sensor_name.isdigit():
            sensor_name = int(sensor_name)

        key = ".".join([
            str(name), 
            "sensors",
            sensor.get("metric"),
            str(sensor_name),
            "device"
        ])

        saved_as_dict = self.update_or_create(sensor, key)

        # for load from file
        if not only_db:
            result = self.dump_to_file(name, dict(saved_as_dict), sensor.get("type"))

        return saved_as_dict

    def save_plan(self, name, plan, key="sensors", only_db=False):
        """dump plan into dile
        """
        result = self.dump_to_file(name, plan, key, "plans")
        return result

    def save_system(self, name, system, key="sensors", only_db=False):
        """dump system into file
        """
        result = self.dump_to_file(name, system, key, "systems")
        return result

    def save_host(self, name, system, key="sensors", only_db=False):
        """method save host into file
        """
        result = self.dump_to_file(name, system, key, "systems")
        return result

    def save_actuator(self, host, actuator):
        key = self.uuid(host, "actuators")

        if not actuator.get("system_plan", None) \
            or (actuator.get("device", None) is None \
            and actuator.get("name", None) is None):
            raise Exception(
                "missing actuator device or system_plan %s" % actuator)

        key = ".".join(
            [str(host),
            "actuators",
            actuator["plan"],
            "device"])

        saved_as_dict = self.update_or_create(actuator, key)

        return saved_as_dict

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

    def delete(self, name, data, key="sensors", attr="devices"):
        """delete object from file
        
        attr = plans, systems, devices

        .. code-block:: yaml
            obj = { id: 10 } or name / device
        """
        deleted = False
        
        items = getattr(self, attr) # copy local devices

        for id, system in getattr(self, attr).iteritems():
            if id in name:
                _dict = system.get(key)
                
                _name = data.pop("id", None)
                
                if not _name:
                    _name = data.get("name", data.get("device", None))
                
                if not _name:
                    raise Exception("missing id, name or device %s" % data)

                # actuator or sensor
                if _name in _dict:
                    _dict.pop(_name)
                    deleted = True
                elif name in items:
                    # host
                    items.pop(name)
                    deleted = True

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
                
                _name = data.pop("id", None)
                
                if not _name:
                    _name = data.get("name", data.get("device", None))
                
                if not _name:
                    raise Exception("missing id, name or device %s" % data)

                _dict[_name] = data
                items[id][key] = _dict

                created = False # switch to update

        if created:
            self.save_meta(
                name,
                data,
                attr
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
        """
            for any host
        """
        key = ".".join([
            host,
            "sensors",
            "*",
            "*",
            "device",
            ])

        keys = self.database.keys(key)
        sensors = []
        for _key in keys:
            _sensor = self.database.hgetall(_key)
            sensors.append(_sensor)

        if len(sensors) == 0:
            # load all sensors
            # returns sensors for all hosts !!
            self.load_sensors()
            sensors = self.sensors # recursive call
            return sensors

        return list(sensors)

    @property
    def sensors(self):
        """return list of sensors by key hostname.sensors
        default to self.hostname
        if sensors is empty method call load_sensors from file
        """

        key = ".".join([
            self.hostname.replace(".", "_"),
            "sensors",
            "*",
            "*",
            "device",
            ])

        keys = self.database.keys(key)
        sensors = []
        for _key in keys:
            _sensor = self.database.hgetall(_key)
            sensors.append(_sensor)

        if len(sensors) == 0:
            # load all sensors
            # returns sensors for all hosts !!
            result = self.load_sensors()
            if not len(result) == 0:
                return self.sensors

        return list(sensors)

    @property
    def actuators(self):
        """return list of sensors by key hostname.sensors
        default to self.hostname
        if sensors is empty method call load_sensors from file
        """

        key = ".".join([
            "*",
            "actuators",
            "*",
            "*",
            "device",
            ])

        keys = self.database.keys(key)
        actuators = []
        for _key in keys:
            _actuator = self.database.hgetall(_key)
            actuators.append(_actuator)

        if len(actuators) == 0:
            result = self.load_actuators()
            if not len(result) == 0:
                return self.actuators # recursive call
                
        return list(actuators)

    def load_actuators(self):
        """return actuators for all systems, but add `system_name` variable"""

        actuators = []

        for system_name, system in self.systems.iteritems():
            for uuid, actuator in system.get('actuators').iteritems():

                if isinstance(actuator['name'], int):
                    actuator['name'] = str(actuator["name"])

                actuator['system_name'] = system_name
                actuator['system_plan'] = system.get('plan')
                merged_dict = dict(actuator.items() + self.get_actuator_device(actuator).items())
                actuators.append(merged_dict)
                self.save_actuator(system_name.replace(".", "_"), actuator)  # save to db

        LOG.debug(actuators)

        return actuators

    def update_or_create(self, obj, key):
        """method accept list or dict
        both save into redis as Dict or List
        if instance is a list method automaticaly update list in redis
        """

        if isinstance(obj, dict):
            # save dictionary
            try:
                saved = self.database.hmset(key, obj) #Dict(instance, key=key, redis=self.database)
            except Exception, e:
                raise e

            return saved
        else:
            saved = self.database.set(key, obj) #Dict(instance, key=key, redis=self.database)
            return saved
        raise Exception("only dict or value is supported")

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

        for host, system in self.devices.iteritems():

            for name, sensor in system.get('sensors').iteritems():

                # check required fields
                if not "metric" in sensor:
                    raise Exception("missing sensor metric field %s" % sensor)

                if not "name" in sensor:
                    sensor["name"] = name

                sensor['os_family'] = self.config.get("os_family")
                sensor['cpu_arch'] = self.config.get("cpu_arch")
                sensor['hostname'] = host
                sensors.append(sensor)
                self.save_sensor(host.replace(".", "_"), sensor, only_db=True)  # save to db
            
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
        for hostname, system in self.systems.iteritems():
            system["name"] = hostname.replace(".", "_")  # hotfix
            for plan_name, plan in self.plans.iteritems():
                plan["name"] = plan_name # hotfix
                if plan_name == system.get("plan"):
                    results.append((system, plan),)
        return results

    def get_plan(self, device_name, device_metric=None):
        """return tuple (system, plan)
        """

        result = (None, None)

        for name, system in self.systems.iteritems():

            system["name"] = name  # hotfix

            for uuid, sensor in system.get('sensors').iteritems():
                if device_metric \
                    and "metric" in sensor:
                    if (sensor.get('device', None) == device_name
                       or sensor.get('name', None) == device_name) \
                        and sensor.get("metric") == device_metric:
                        result = system, sensor.get('plan')
                else:
                    if sensor.get('name') == device_name:
                        result = system, sensor.get('plan')
        if None in result:
            LOG.error("device_name: %s & device_metric: %s " % (device_name, device_metric))
        return result

    def get_actuator_device(self, actuator):
        """return actuator from host devices"""

        for name, host in self.devices.iteritems():
            for uuid, device in host.get('actuators').iteritems():
                if ("actuator" in actuator and actuator["actuator"] == uuid) \
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

    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    """


settings = RoboticeSettings()  # one true Settings


def setup_app(worker):
    """dealing with global singleton and load configs
    easiest way how you get settings instance is RoboticeSettings('reasoner')
    """
    global settings

    settings.setup_app(worker)

    return settings
