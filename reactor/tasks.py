
from celery.task import task
from celery.signals import celeryd_after_setup
 
from utils import get_grains, import_module, setup_app

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


@celeryd_after_setup.connect
def init_reactors(sender, instance, **kwargs):

    config = setup_app('reasoner')

    for host in config.devices:
        for actuator in host.get('actuators'):
            if actuator.has_key('default'):
                if actuator.get('default') == 'off':
                    model_value = 0
                    real_value = 1
                else:
                    model_value = 1
                    real_value = 0
                send_task('reactor.commit_action', [config, actuator, str(model_value), str(real_value)], {})
