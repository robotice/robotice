#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import routes

from robotice.api.v1 import tasks
from robotice.api import wsgi
from robotice.common.i18n import _


class API(wsgi.Router):

    """
    WSGI router for Heat v1 ReST API requests.

    ..code-block: bash
        
        /task/list/reactor
        /task/send/reactor/commit.action
        /task/info/reactor/asdad-asdad-asdad
        /task/result/reactor/asdad-asdad-asdad

    """

    def __init__(self, conf, **local_conf):
        self.conf = conf
        mapper = routes.Mapper()

        task_resource = tasks.create_resource(conf)
        with mapper.submapper(controller=task_resource,
                              path_prefix="/task") as task_mapper:

            # Tasks
            task_mapper.connect("task",
                                 "/list/{role}",
                                 action="task_list",
                                 conditions={'method': 'GET'})
            task_mapper.connect("task",
                                 "/send/{role}/{taskname}",
                                 action="send_task",
                                 conditions={'method': 'POST'})
            task_mapper.connect("task",
                                 "/info/{role}/{task_id}",
                                 action="task_info",
                                 conditions={'method': 'GET'})
            task_mapper.connect("task",
                                 "/result/{role}/{task_id}",
                                 action="task_result",
                                 conditions={'method': 'GET'})

        # Plans
        
        # Devices

        # Systems

        # Events

        # Actions

        super(API, self).__init__(mapper)