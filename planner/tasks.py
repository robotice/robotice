from yaml import load
from celery.task import task

@task(name='planner.get_model_data')
def get_model_data(config):
    return config.plans

def get_plan(config):
	"""pro dany system vrati plan"""
	for system in config.systems:
        for plan in config.config.plans:
			if system.get("name") == plan.get("name"):
        		for _plan in config.plans:
        			if _plan.get("name") == system.get("plan"):
                		return _plan
    return None

@task(name='planner.return_model_data')
def return_model_data(config):
    values = []
    return get_plan(config)