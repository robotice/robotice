#
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2013 IBM Corp.
# All Rights Reserved.
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
Utility methods for serializing responses
"""

import datetime
import json

import six

import logging

LOG = logging.getLogger(__name__)


class JSONResponseSerializer(object):

    def to_json(self, data):
        def sanitizer(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            return obj

        response = json.dumps(data, default=sanitizer)
        LOG.debug("JSON response : %s" % response)
        return response

    def default(self, response, result):
        response.content_type = 'application/json'
        response.body = self.to_json(result)


# Escape XML serialization for these keys, as the AWS API defines them as
# JSON inside XML when the response format is XML.
JSON_ONLY_KEYS = ('TemplateBody', 'Metadata')
