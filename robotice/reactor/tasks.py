import subprocess

from celery.task import task

from robotice.utils.functional import import_module
from robotice.conf import settings

@task(name='reactor.commit_action')
def commit_action(actuator, model_data, real_data=None, settings=None):
    """
    actuator = dict:{device:sispm}

    for actuator must exist module:actuator.py for example sispm.actuator.py

    """

    LOG = commit_action.get_logger()


    mod = import_module(
        actuator.get("device"),
        "actuator",
        method="run")

    try:
        settings.setup_app("reactor")
        actuator['architecture'] = settings.config["cpu_arch"]
        actuator['os_family'] = settings.config["os_family"]        
    except Exception, e:
        # must be prived from actuator["os_family"]
        pass

    LOG.debug([actuator, model_data, real_data])

    try:
        command, results = mod.run(actuator, model_data, real_data)
    except Exception, ex:
        raise ex

    LOG.info(command)
    LOG.info(results)

    return results

@task(name='reactor.run')
def run(time=60):
    """
    """

    LOG = run.get_logger()

    import time 

    ticks = 0

    test = "ticks += 1"

    while ticks != time:


        if not run.request.called_directly:
            run.update_state(state='PROGRESS',
                meta={'current': ticks, 'total': time})
        
        ticks += 1
        time.sleep(1)
    
    return "Your toast is baked !"
