def get_plan(config, device_name, device_metric):
    """pro dany system vrati plan"""
    for system in config.systems:
        for sensor in system.get('sensors'):
            if device_name == sensor.get('device'):
                return system, sensor.get('plan')
    return None, None

def get_actuator_device(config, device_name):
    """pro dany system vrati plan"""
    for host in config.devices:
        for device in host.get('actuators'):
            if device_name == device.get('name'):
                return device
    return None

def get_actuators(config):
    """pro dany system vrati plan"""
    actuators = []
    for system in config.systems:
        for actuator in system.get('actuators'):
            actuator['system_name'] = system.get('name')
            actuator['system_plan'] = system.get('plan')
            actuators.append(actuator)
    return actuators