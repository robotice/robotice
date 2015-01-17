from yaml import load
from celery.task import task
import datetime
from math import floor

@task(name='planner.get_model_data')
def get_model_data(config):
    """pra dany cyklus a soucasny cas ukladala modelova data do redisu
       db_key = "{0}.{1}.{2}.{3}".format(system.get('name'), 'sensors', device.get('name'), 'model')
    """
    logger = get_model_data.get_logger()

    for system, plan in config.get_system_plans:

        devices = plan.get('sensors')
        start = datetime.datetime.strptime(str(system.get('start')), "%Y-%m-%d %H:%M:%S")
        logger.info("{0}".format(start))
        now = datetime.datetime.now()
        plan_cycle = int(plan.get('cycle'))
        total_time_delta = now - start
        relative = floor(total_time_delta.seconds / plan_cycle)
        time_delta = total_time_delta.seconds - (relative * plan_cycle)

        for uuid, device in plan.get('sensors').iteritems():
            db_key = ":".join([
                system.get('name'),
                (device.get('name', None) or uuid),
                'model'])
            value, values = 0, (0, 0)

            for cycle in device.get('cycles'):
                cycle_start = int(cycle.get('start'))#datetime.datetime.strptime(str(cycle.get('start')), "%H:%M:%S")
                cycle_end = int(cycle.get('end'))#datetime.datetime.strptime(str(cycle.get('end')), "%H:%M:%S")
                if (time_delta > cycle_start) and (time_delta < cycle_end):
                    if cycle.has_key('value'):
                        value = cycle.get('value')
                    else:
                        values = (cycle.get('value_low'), cycle.get('value_high'))

                    if cycle.has_key('value'):
                        config.metering.send(db_key, value)
                        config.database.set(db_key, value)
                        logger.info(value)
                    else:
                        config.metering.send("%s_%s"% (db_key, "low"), values[0])
                        config.metering.send("%s_%s"% (db_key, "high"), values[1])
                        config.database.set(db_key, values)
                        logger.info(values)
    return []

@task(name='planner.return_model_data')
def return_model_data(config):
    values = []
    return []