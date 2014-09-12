
from celery.task import task
 
from robotice.utils.functional import import_module

@task(name='reactor.commit_action')
def commit_action(config, actuator, model_data, real_data):

    LOG = commit_action.get_logger()

    mod = import_module(actuator.get("device"))

    actuator['architecture'] = config["cpu_arch"]
    actuator['os_family'] = config["os_family"]

    LOG.info([actuator, model_data, real_data])

    command, results = mod.run(actuator, model_data, real_data)

    LOG.info(command)
    LOG.info(results)

    return results
