
"""
base object managers

"""

import sys
import logging

from robotice.conf.managers.base import BaseManager

LOG = logging.getLogger(__name__)

import glob
from yaml import load, dump, safe_dump

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


actions = ActionManager()        