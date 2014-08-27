
from celery.task import task
 
from conf import get_grains, import_module, setup_app

@task(name='reactor.commit_action')
def commit_action(config, actuator, model_data, real_data):

    logger = commit_action.get_logger()

    module_name = ".".join(["reactor", "actuators", actuator.get("device")])

    mod = import_module(module_name)

    grains = get_grains()

    actuator['architecture'] = grains.cpu_arch

    logger.info([actuator, model_data, real_data])

    command, results = mod.run(actuator, model_data, real_data)

    logger.info(command)
    logger.info(results)

    return results
