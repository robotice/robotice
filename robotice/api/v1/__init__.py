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
    """

    def __init__(self, conf, **local_conf):
        self.conf = conf
        mapper = routes.Mapper()

        tasks_resource = tasks.create_resource(conf)
        with mapper.submapper(controller=tasks_resource,
                              path_prefix="/{tenant_id}") as task_mapper:
            # Tasks
            task_mapper.connect("tasks",
                                 "/validate",
                                 action="validate_template",
                                 conditions={'method': 'POST'})
            task_mapper.connect("resource_types",
                                 "/resource_types",
                                 action="list_resource_types",
                                 conditions={'method': 'GET'})
            task_mapper.connect("resource_schema",
                                 "/resource_types/{type_name}",
                                 action="resource_schema",
                                 conditions={'method': 'GET'})
            task_mapper.connect("generate_template",
                                 "/resource_types/{type_name}/template",
                                 action="generate_template",
                                 conditions={'method': 'GET'})

            # Stack collection
            task_mapper.connect("stack_index",
                                 "/tasks",
                                 action="index",
                                 conditions={'method': 'GET'})
            task_mapper.connect("stack_create",
                                 "/tasks",
                                 action="create",
                                 conditions={'method': 'POST'})
            task_mapper.connect("stack_preview",
                                 "/tasks/preview",
                                 action="preview",
                                 conditions={'method': 'POST'})
            task_mapper.connect("stack_detail",
                                 "/tasks/detail",
                                 action="detail",
                                 conditions={'method': 'GET'})

            # Stack data
            task_mapper.connect("stack_lookup",
                                 "/tasks/{stack_name}",
                                 action="lookup")
            # \x3A matches on a colon.
            # Routes treats : specially in its regexp
            task_mapper.connect("stack_lookup",
                                 r"/tasks/{stack_name:arn\x3A.*}",
                                 action="lookup")
            subpaths = ['resources', 'events', 'template', 'actions']
            path = "{path:%s}" % '|'.join(subpaths)
            task_mapper.connect("stack_lookup_subpath",
                                 "/tasks/{stack_name}/" + path,
                                 action="lookup",
                                 conditions={'method': 'GET'})
            task_mapper.connect("stack_lookup_subpath_post",
                                 "/tasks/{stack_name}/" + path,
                                 action="lookup",
                                 conditions={'method': 'POST'})
            task_mapper.connect("stack_show",
                                 "/tasks/{stack_name}/{stack_id}",
                                 action="show",
                                 conditions={'method': 'GET'})
            task_mapper.connect("stack_template",
                                 "/tasks/{stack_name}/{stack_id}/template",
                                 action="template",
                                 conditions={'method': 'GET'})

            # Stack update/delete
            task_mapper.connect("stack_update",
                                 "/tasks/{stack_name}/{stack_id}",
                                 action="update",
                                 conditions={'method': 'PUT'})
            task_mapper.connect("stack_update_patch",
                                 "/tasks/{stack_name}/{stack_id}",
                                 action="update_patch",
                                 conditions={'method': 'PATCH'})
            task_mapper.connect("stack_delete",
                                 "/tasks/{stack_name}/{stack_id}",
                                 action="delete",
                                 conditions={'method': 'DELETE'})

            # Stack abandon
            task_mapper.connect("stack_abandon",
                                 "/tasks/{stack_name}/{stack_id}/abandon",
                                 action="abandon",
                                 conditions={'method': 'DELETE'})

            task_mapper.connect("stack_snapshot",
                                 "/tasks/{stack_name}/{stack_id}/snapshots",
                                 action="snapshot",
                                 conditions={'method': 'POST'})

            task_mapper.connect("stack_snapshot_show",
                                 "/tasks/{stack_name}/{stack_id}/snapshots/"
                                 "{snapshot_id}",
                                 action="show_snapshot",
                                 conditions={'method': 'GET'})

            task_mapper.connect("stack_snapshot_delete",
                                 "/tasks/{stack_name}/{stack_id}/snapshots/"
                                 "{snapshot_id}",
                                 action="delete_snapshot",
                                 conditions={'method': 'DELETE'})

            task_mapper.connect("stack_list_snapshots",
                                 "/tasks/{stack_name}/{stack_id}/snapshots",
                                 action="list_snapshots",
                                 conditions={'method': 'GET'})

            task_mapper.connect("stack_snapshot_restore",
                                 "/tasks/{stack_name}/{stack_id}/snapshots/"
                                 "{snapshot_id}/restore",
                                 action="restore_snapshot",
                                 conditions={'method': 'POST'})

        # Plans
        
        # Devices

        # Systems

        # Events

        # Actions

        super(API, self).__init__(mapper)