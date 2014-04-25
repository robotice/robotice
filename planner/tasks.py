from yaml import load
from celery.task import task
import datetime
from math import floor

def get_plan(config):
    """pro dany system vrati plan"""
    for system in config.systems:
        for plan in config.plans:
            if plan.get("name") == system.get("plan"):
                return system, plan
    return None

@task(name='planner.get_model_data')
def get_model_data(config):
    system, plan = get_plan(config)
    devices = plan.get('actuators') + plan.get('sensors')
    start = datetime.datetime.strptime(str(system.get('start')), "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    plan_cycle = int(plan.get('cycle'))
    for device in devices:
        for cycle in device.get('cycles'):
            cycle_start = int(cycle.get('start'))#datetime.datetime.strptime(str(cycle.get('start')), "%H:%M:%S")
            cycle_end = int(cycle.get('end'))#datetime.datetime.strptime(str(cycle.get('end')), "%H:%M:%S")
        path = "{0}.{1}.{2}.{3}".format(system.get('name'), 'actuator', device.get('name'), 'model')
        time_delta = now - start
        relative = floor(time_delta.seconds / plan_cycle)
        time_delta_ = relative - relative
        value, values = 0, (0, 0)
        if (time_delta_ > cycle_start) and (time_delta_ < cycle_end):
            if cycle.has_key('value'):
                value = cycle.get('value')
            else:
                values = (cycle.get('value_low'), cycle.get('value_high'))
        if cycle.has_key('value'):
            config.database.set(path, value)
        else:
            config.database.set(path, values)
    return time_delta

@task(name='planner.return_model_data')
def return_model_data(config):
    values = []
    return