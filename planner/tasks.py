from yaml import load
from celery.task import task

def get_plan(config):
    """pro dany system vrati plan"""
    for system in config.systems:
        for plan in config.config.get("plans"):
            if system.get("name") == plan.get("name"):
                for _plan in config.plans:
                    if _plan.get("name") == system.get("plan"):
                        return _plan
    return None

@task(name='planner.get_model_data')
def get_model_data(config):
    plan = get_plan(config)
    devices = plan.get('actuators') + plan.get('sensors')
    for device in devices:
    	for cycle in device.get('cycles'):
        	return cycle
    return devices

@task(name='planner.return_model_data')
def return_model_data(config):
    values = []
    return