
from celery.task import task
 
@task(name='reactor.commit_action')
def commit_action(config, actuator, model_data, real_data):


def get_sensor_data(config, sensor, grains):

    module_name = ".".join(["reactor", "actuators", actuator.get("device")])

    mod = import_module(module_name)

    results = mod.run(actuator, model_data, real_data)

    return results
