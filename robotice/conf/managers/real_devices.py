
"""
base object managers

"""

import sys
import logging

from robotice.conf.managers.base import BaseManager

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend

import glob
from yaml import load, dump, safe_dump

LOG = logging.getLogger(__name__)

# move to config
CONFIG_DIR = "/srv/robotice/config"
ACTION_DIR = "actions"


class ActionManager(BaseManager):

    def list(self):
        """load and return all actions from local storage
        """

        path = "/".join([CONFIG_DIR, ACTION_DIR])

        actions = []

        for path in glob.glob("/".join([path, '*.yml'])):
            try:
                f = open(path, 'r')
                raw_data = load(f)
                for id, action in raw_data.iteritems():
                    action["id"] = id
                    actions.append(action)
            except Exception, e:
                raise e

        return actions


    def get(self, action_id):
        """return action if is founded
        """

        for action in self.list():

            if str(action["id"]) == str(action_id):
                return action

        return None

    def save(self, id, action):
        """save action to disk

        TODO: recursive dump with indentation

        """

        path = "/".join([CONFIG_DIR, ACTION_DIR])
        paths = glob.glob("/".join([path, '*.yml']))

        created = True

        for path in paths:
            try:
                f = open(paths[0], 'r')
                raw_data = load(f)
                f.close()
                for _id, _action in raw_data.iteritems():
                    if str(_id) == str(id):
                        _old = _action
                        try:
                            action["options"] = load(action["options"])
                        except Exception, e:
                            raise e
                        _old.update(action)
                        raw_data[_id] = _old
                        if not "id" in action:
                            action["id"] = id

                        with open(path, 'w') as yaml_file:
                            safe_dump(raw_data, yaml_file, default_flow_style=False, allow_unicode=True)
                            created = False
            except Exception, e:
                raise e

        if created:

            try:
                f = open(paths[0], 'r')
                raw_data = load(f)
                f.close()
                raw_data[id] = action

                with open(paths[0], 'w') as yaml_file:
                    safe_dump(raw_data, yaml_file, default_flow_style=False)
            except Exception, e:
              raise e

        return True

    def do(self, action_id):
        """Execute a action by name(uuid) (doesn't require task sources)

        """

        action = actions.get(action_id)

        if not action:
            return {"status": 404, "error": "Action %s not founded." % action_id}
        LOG.debug(action)

        app = self.capp()

        args, kwargs, options = self._get_task_args(action.get("options"))
        command = action.get("command", None)
        LOG.error(args)
        LOG.debug("Invoking task '%s' with '%s' and '%s'",
                  command, args, kwargs)

        result = app.send_task(
            command, args=args, kwargs=kwargs, **options)
        response = {'task-id': result.task_id}

        response["action"] = action

        if self.backend_configured(result):
            response.update(state=result.state)

        return response

    def backend_configured(self, result):
        return not isinstance(result.backend, DisabledBackend)

    def _get_task_args(self, body):
        """helper which return task args, kwargs and options
        """

        try:
            options = body
            if isinstance(body, basestring):
                options = json.loads(body)
            args = options.pop('args', [])
            kwargs = options.pop('kwargs', {})
        except Exception, e:
            raise exc.HTTPBadRequest(str(e))

        if not isinstance(args, (list, tuple)):
            try:
                args = args.values()
                return args, kwargs, options
            except Exception, e:
                raise e
            raise exc.HTTPBadRequest('args must be an array')

        return args, kwargs, options


actions = ActionManager()        