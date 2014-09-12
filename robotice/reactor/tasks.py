import subprocess

from celery.task import task

from robotice.utils.functional import import_module


@task(name='reactor.commit_action')
def commit_action(config, actuator, model_data, real_data):

    LOG = commit_action.get_logger()

    try:
        mod = import_module(
            actuator.get("device"),
            "actuator",
            driver_path="/srv/robotice/actuators")
    except ImportError:
        LOG.error("Could not import actuator %s" % actuator.get("device"))

    actuator['architecture'] = config["cpu_arch"]
    actuator['os_family'] = config["os_family"]

    LOG.debug([actuator, model_data, real_data])

    try:
        command, results = mod.run(actuator, model_data, real_data)
    except Exception, ex:
        raise ex

    LOG.info(command)
    LOG.info(results)

    return results
