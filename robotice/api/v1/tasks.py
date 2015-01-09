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

"""
Stack endpoint for Heat v1 ReST API.
"""

import six
import logging
from six.moves.urllib import parse
from webob import exc

from robotice.utils import serializers
from robotice.api import wsgi

from robotice.common.i18n import _

LOG = logging.getLogger(__name__)

#TODO implement https://repo1.robotice.cz/robotice/control-daemon/blob/develop/robotice_control/api/tasks.py

class InstantiationData(object):
    """
    The data accompanying a PUT or POST request to create or update a stack.
    """

    PARAMS = (
        PARAM_STACK_NAME,
        PARAM_TEMPLATE,
        PARAM_TEMPLATE_URL,
        PARAM_USER_PARAMS,
        PARAM_ENVIRONMENT,
        PARAM_FILES,
    ) = (
        'stack_name',
        'template',
        'template_url',
        'parameters',
        'environment',
        'files',
    )

    def __init__(self, data, patch=False):
        """
        Initialise from the request object.
        If called from the PATCH api, insert a flag for the engine code
        to distinguish.
        """
        self.data = data

    @staticmethod
    def format_parse(data, data_type):
        """
        Parse the supplied data as JSON or YAML, raising the appropriate
        exception if it is in the wrong format.
        """

        try:
            if data_type == 'Environment':
                return environment_format.parse(data)
            else:
                return template_format.parse(data)
        except ValueError as parse_ex:
            mdict = {'type': data_type, 'error': six.text_type(parse_ex)}
            msg = _("%(type)s not in valid format: %(error)s") % mdict
            raise exc.HTTPBadRequest(msg)

    def stack_name(self):
        """
        Return the stack name.
        """
        if self.PARAM_STACK_NAME not in self.data:
            raise exc.HTTPBadRequest(_("No stack name specified"))
        return self.data[self.PARAM_STACK_NAME]

    def template(self):
        """
        Get template file contents, either inline, from stack adopt data or
        from a URL, in JSON or YAML format.
        """
        if self.PARAM_TEMPLATE in self.data:
            template_data = self.data[self.PARAM_TEMPLATE]
            if isinstance(template_data, dict):
                return template_data
        elif self.PARAM_TEMPLATE_URL in self.data:
            url = self.data[self.PARAM_TEMPLATE_URL]
            LOG.debug('TemplateUrl %s' % url)
            try:
                template_data = urlfetch.get(url)
            except IOError as ex:
                err_reason = _('Could not retrieve template: %s') % ex
                raise exc.HTTPBadRequest(err_reason)
        else:
            raise exc.HTTPBadRequest(_("No template specified"))

        return self.format_parse(template_data, 'Template')

    def environment(self):
        """
        Get the user-supplied environment for the stack in YAML format.
        If the user supplied Parameters then merge these into the
        environment global options.
        """
        env = {}
        if self.PARAM_ENVIRONMENT in self.data:
            env_data = self.data[self.PARAM_ENVIRONMENT]
            if isinstance(env_data, dict):
                env = env_data
            else:
                env = self.format_parse(env_data,
                                        'Environment')

        environment_format.default_for_missing(env)
        parameters = self.data.get(self.PARAM_USER_PARAMS, {})
        env[self.PARAM_USER_PARAMS].update(parameters)
        return env

    def files(self):
        return self.data.get(self.PARAM_FILES, {})

    def args(self):
        """
        Get any additional arguments supplied by the user.
        """
        params = self.data.items()
        return dict((k, v) for k, v in params if k not in self.PARAMS)


class StackController(object):
    """
    WSGI controller for stacks resource in Heat v1 API
    Implements the API actions
    """
    # Define request scope (must match what is in policy.json)
    REQUEST_SCOPE = 'stacks'

    def __init__(self, options):
        self.options = options

    def default(self, req, **args):
        raise exc.HTTPNotFound()

    def _index(self, req, tenant_safe=True):
        filter_whitelist = {
            'status': 'mixed',
            'name': 'mixed',
            'action': 'mixed',
            'tenant': 'mixed',
            'username': 'mixed',
            'owner_id': 'mixed',
        }
        whitelist = {
            'limit': 'single',
            'marker': 'single',
            'sort_dir': 'single',
            'sort_keys': 'multi',
            'show_deleted': 'single',
            'show_nested': 'single',
        }
        params = req.params
        filter_params = req.params

        show_deleted = False
        if rpc_api.PARAM_SHOW_DELETED in params:
            params[rpc_api.PARAM_SHOW_DELETED] = param_utils.extract_bool(
                params[rpc_api.PARAM_SHOW_DELETED])
            show_deleted = params[rpc_api.PARAM_SHOW_DELETED]
        show_nested = False
        if rpc_api.PARAM_SHOW_NESTED in params:
            params[rpc_api.PARAM_SHOW_NESTED] = param_utils.extract_bool(
                params[rpc_api.PARAM_SHOW_NESTED])
            show_nested = params[rpc_api.PARAM_SHOW_NESTED]
        # get the with_count value, if invalid, raise ValueError
        with_count = False
        if req.params.get('with_count'):
            with_count = param_utils.extract_bool(
                req.params.get('with_count'))

        if not filter_params:
            filter_params = None

        stacks = self.rpc_client.list_stacks(req.context,
                                             filters=filter_params,
                                             tenant_safe=tenant_safe,
                                             **params)

        count = None
        if with_count:
            try:
                # Check if engine has been updated to a version with
                # support to count_stacks before trying to use it.
                count = self.rpc_client.count_stacks(req.context,
                                                     filters=filter_params,
                                                     tenant_safe=tenant_safe,
                                                     show_deleted=show_deleted,
                                                     show_nested=show_nested)
            except AttributeError as exc:
                LOG.warn(_LW("Old Engine Version: %s") % exc)

        return stacks_view.collection(req, stacks=stacks, count=count,
                                      tenant_safe=tenant_safe)

    def list_resource_types(self, req):
        """
        Returns a list of valid resource types that may be used in a template.
        """
        support_status = req.params.get('support_status')
        return {}

class StackSerializer(serializers.JSONResponseSerializer):
    """Handles serialization of specific controller method responses."""

    def _populate_response_header(self, response, location, status):
        response.status = status
        response.headers['Location'] = location.encode('utf-8')
        response.headers['Content-Type'] = 'application/json'
        return response

    def create(self, response, result):
        self._populate_response_header(response,
                                       result['stack']['links'][0]['href'],
                                       201)
        response.body = self.to_json(result)
        return response


def create_resource(options):
    """
    Stacks resource factory method.
    """
    deserializer = wsgi.JSONRequestDeserializer()
    serializer = StackSerializer()
    return wsgi.Resource(StackController(options), deserializer, serializer)