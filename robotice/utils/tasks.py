
from __future__ import absolute_import

from celery import Task

from celery.events.state import Task as StateTask

import logging

LOG = logging.getLogger(__name__)

def iter_tasks(events, limit=None, type=None, worker=None, state=None):
    i = 0

    for uuid, task in events.tasks_by_timestamp():
        if type and task.name != type:
            continue
        if worker and task.worker and task.worker.hostname != worker:
            continue
        if state and task.state != state:
            continue
        yield uuid, task
        i += 1
        if i == limit:
            break


def get_task_by_id(events, task_id):
    if hasattr(StateTask, '_fields'):  # Old version
        return events.tasks.get(task_id)
    else:
        _fields = StateTask._defaults.keys()
        task = events.tasks.get(task_id)
        if task is not None:
            task._fields = _fields
        return task

class DebugTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        print('TASK STARTING: {0.name}[{0.request.id}]'.format(self))
        return super(DebugTask, self).__call__(*args, **kwargs)