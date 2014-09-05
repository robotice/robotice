
from celery.task import task
 
from conf.grains import grains
from utils.functional import import_module

@task(name='reactor.commit_action')
def commit_action(actuator, model_data, real_data):

    LOG = commit_action.get_logger()

    module_name = ".".join(["reactor", "actuators", actuator.get("device")])

    mod = import_module(module_name)

    actuator['architecture'] = grains.cpu_arch

    LOG.info([actuator, model_data, real_data])

    command, results = mod.run(actuator, model_data, real_data)

    LOG.info(command)
    LOG.info(results)

    return results
