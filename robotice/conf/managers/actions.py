
"""
base object managers

"""

import sys
import logging

from robotice.conf.managers import base

from celery import states
from celery import Celery
from celery.result import AsyncResult
from celery.backends.base import DisabledBackend

import glob
from yaml import load, dump, safe_dump

LOG = logging.getLogger(__name__)


class ActionManager(base.BaseConfigManager, base.CeleryManager):

    # move to config
    config_path = "actions/*.yml"

    def do(self, action_id):
        """Execute a action by name(uuid) (doesn't require task sources)

        """

        action = actions.get(action_id)

        if not action:
            return {"status": 404, "error": "Action %s not found." % action_id}
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