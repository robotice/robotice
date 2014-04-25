from yaml import load
from celery.task import task
from dateutil import parser
import datetime

def get_plan(config):
    """pro dany system vrati plan"""
    for system in config.systems:
        for plan in config.config.get("plans"):
            if system.get("name") == plan.get("name"):
                for _plan in config.plans:
                    if _plan.get("name") == system.get("plan"):
                        return system, _plan
    return None

@task(name='planner.get_model_data')
def get_model_data(config):
    system, plan = get_plan(config)
    devices = plan.get('actuators') + plan.get('sensors')
    start = datetime.datetime.strptime(str(system.get('start')), "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()

    for device in devices:
        for cycle in device.get('cycles'):
            cycle_start = int(cycle.get('start'))#datetime.datetime.strptime(str(cycle.get('start')), "%H:%M:%S")
            cycle_end = int(cycle.get('end'))#datetime.datetime.strptime(str(cycle.get('end')), "%H:%M:%S")
            cycle_delta = cycle_end - cycle_start
        path = "{0}.{1}.{2}".format(system.get('name'), 'actuator', device.get('name'))
        time_delta = now - start
        relative = time_delta / cycle_delta
    return time_delta

@task(name='planner.return_model_data')
def return_model_data(config):
    values = []
    return