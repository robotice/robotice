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
from robotice.api import wsgi
from robotice.common.i18n import _

from robotice.api.v1.tasks import TaskController
from robotice.api.v1.actions import ActionController
from robotice.api.v1.workers import WorkerController
from robotice.api.v1.devices import DeviceController
from robotice.api.v1.systems import SystemController
from robotice.api.v1.plans import PlanController
from robotice.api.v1 import workers


class API(wsgi.Router):

    """
    WSGI router for Heat v1 ReST API requests.

    Every stable endpoint has GET, POST, PUT, DELETE

    ..code-block: bash
        
        GET /plan
        GET /plan/{id}
        DELETE /plan/{id}
        POST /plan
        /system...
        /device...
        /action
        POST /action/do/{id}

    """

    def __init__(self, conf, **local_conf):
        self.conf = conf
        mapper = routes.Mapper()

        # Actions
        action_resource = ActionController.create_resource(conf)
        with mapper.collection(collection_name="actions", resource_name="action",
                          path_prefix="/action", controller=action_resource) as action_mapper:

            action_mapper.connect("action",
                                 "/do/{id}",
                                 action="do",
                                 conditions={'method': 'POST'})

        # Devices, Plans, Systems

        plan_resource = PlanController.create_resource(conf)

        mapper.collection(collection_name="plans", resource_name="plan",
                          path_prefix="/plan", controller=plan_resource)

        device_resource = DeviceController.create_resource(conf)

        mapper.collection(collection_name="devices", resource_name="device",
                          path_prefix="/device", controller=device_resource)

        system_resource = SystemController.create_resource(conf)
        mapper.collection(collection_name="systems", resource_name="system",
                          path_prefix="/system", controller=system_resource)

        # Celery tasks
        # unstable endpoints !

        task_resource = TaskController.create_resource(conf)
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

        # Workers
        worker_resource = WorkerController.create_resource(conf)
        with mapper.submapper(controller=worker_resource,
                              path_prefix="/worker") as worker_mapper:

            worker_mapper.connect("worker",
                                 "/list",
                                 action="worker_list",
                                 conditions={'method': 'GET'})

        super(API, self).__init__(mapper)