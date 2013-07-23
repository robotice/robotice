
from celery.task import task

@task(name='monitor.get_real_data')
def get_real_data(sensors):

    tasks = []

    for sensor in sensors:
        if sensor.get("type") == "dht":
            tasks.append(dht_get_data.delay(sensor))
        elif sensor.get("type") == "sispm":
            tasks.append(sispm_get_data.delay(sensor))
        elif sensor.get("type") == "dummy":
            tasks.append(dummy_get_data.delay(sensor))
   
    return collect_real_data.delay([], tasks)


@task(name='monitor.collect_real_data')
def collect_real_data(results, tasks):

    completed_tasks = []
    for task in tasks:
        if task.ready():
            completed_tasks.append(task)
            results.append(task.get())

    # remove completed tasks
    tasks = list(set(tasks) - set(completed_tasks))

    if len(tasks) > 0:
        # resend the task to execute at least 1 second from now
        collect_real_data.delay(results, tasks, countdown=1)
    else:
        # we done
        return results

@task(name='monitor.dht.get_data')
def dht_get_data(sensor):
    from sensors.dht import get_dht_data

    return ['metrics.value', 24]

@task(name='monitor.dummy.get_data')
def dummy_get_data(sensor):
    from sensors.dummy import get_dummy_data

    return ['metrics2.value', 14]

@task(name='monitor.sispm.get_data')
def get_sispm_data(sensor):
    from sensors.sispm import get_sispm_data

    return ['metrics3.value', 2543]