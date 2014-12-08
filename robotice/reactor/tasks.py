import subprocess

from celery.task import task

from robotice.utils.functional import import_module
from robotice.conf import settings

@task(name='reactor.commit_action')
def commit_action(actuator, model_data, real_data, settings=None):
    """
    actuator = dict:{device:sispm}

    for actuator must exist module:actuator.py for example sispm.actuator.py

    """

    LOG = commit_action.get_logger()

    settings.setup_app("reactor")

    mod = import_module(
        actuator.get("device"),
        "actuator",
        method="run")

    actuator['architecture'] = settings.config["cpu_arch"]
    actuator['os_family'] = settings.config["os_family"]

    LOG.debug([actuator, model_data, real_data])

    try:
        command, results = mod.run(actuator, model_data, real_data)
    except Exception, ex:
        raise ex

    LOG.info(command)
    LOG.info(results)

    return results
