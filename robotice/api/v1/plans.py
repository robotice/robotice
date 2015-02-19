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
Task endpoint for Robotice v1 ReST API.
"""

import logging

from robotice.api.v1.base import GenericController

from robotice.common.i18n import _

LOG = logging.getLogger(__name__)


class PlanController(GenericController):

    """

    load actions from local storage and prodive API for managing it

    """

    REQUEST_SCOPE = 'plans'

    PARAMS = ['name', 'cycle']

    def create(self, req, body={}):
        response = {"status": "ok"}
        LOG.debug(body)

        self.validate(body)

        name = body.pop("name")

        try:
            obj = getattr(self.app, self.REQUEST_SCOPE, None).set(name, body)
        except Exception, e:
            response = {"status": "error", "errors": str(e)}

        return response