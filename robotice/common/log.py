# Copyright 2011 OpenStack Foundation.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
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

"""OpenStack logging handler.
This module adds to logging functionality by adding the option to specify
a context object when calling the various log methods.  If the context object
is not specified, default formatting is used. Additionally, an instance uuid
may be passed as part of the log message, which is intended to make it easier
for admins to find messages related to a specific instance.
It also allows setting of formatting information through conf.
"""

import copy
import inspect
import itertools
import logging
import logging.config
import logging.handlers
import os
import socket
import sys
import traceback

from oslo.config import cfg
from oslo.utils import importutils
import six
from six import moves

_PY26 = sys.version_info[0:2] == (2, 6)

from robotice.common.i18n import _

_DEFAULT_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


common_cli_opts = [
    cfg.BoolOpt('debug',
                short='d',
                default=False,
                help='Print debugging output (set logging level to '
                     'DEBUG instead of default WARNING level).'),
    cfg.BoolOpt('verbose',
                short='v',
                default=False,
                help='Print more verbose output (set logging level to '
                     'INFO instead of default WARNING level).'),
]

logging_cli_opts = [
    cfg.StrOpt('log-config-append',
               metavar='PATH',
               deprecated_name='log-config',
               help='The name of a logging configuration file. This file '
                    'is appended to any existing logging configuration '
                    'files. For details about logging configuration files, '
                    'see the Python logging module documentation.'),
    cfg.StrOpt('log-format',
               metavar='FORMAT',
               help='DEPRECATED. '
                    'A logging.Formatter log message format string which may '
                    'use any of the available logging.LogRecord attributes. '
                    'This option is deprecated.  Please use '
                    'logging_context_format_string and '
                    'logging_default_format_string instead.'),
    cfg.StrOpt('log-date-format',
               default=_DEFAULT_LOG_DATE_FORMAT,
               metavar='DATE_FORMAT',
               help='Format string for %%(asctime)s in log records. '
                    'Default: %(default)s .'),
    cfg.StrOpt('log-file',
               metavar='PATH',
               deprecated_name='logfile',
               help='(Optional) Name of log file to output to. '
                    'If no default is set, logging will go to stdout.'),
    cfg.StrOpt('log-dir',
               deprecated_name='logdir',
               help='(Optional) The base directory used for relative '
                    '--log-file paths.'),
    cfg.BoolOpt('use-syslog',
                default=False,
                help='Use syslog for logging. '
                     'Existing syslog format is DEPRECATED during I, '
                     'and will change in J to honor RFC5424.'),
    cfg.BoolOpt('use-syslog-rfc-format',
                # TODO(bogdando) remove or use True after existing
                #    syslog format deprecation in J
                default=False,
                help='(Optional) Enables or disables syslog rfc5424 format '
                     'for logging. If enabled, prefixes the MSG part of the '
                     'syslog message with APP-NAME (RFC5424). The '
                     'format without the APP-NAME is deprecated in I, '
                     'and will be removed in J.'),
    cfg.StrOpt('syslog-log-facility',
               default='LOG_USER',
               help='Syslog facility to receive log lines.')
]

generic_log_opts = [
    cfg.BoolOpt('use_stderr',
                default=True,
                help='Log output to standard error.')
]

DEFAULT_LOG_LEVELS = ['amqp=WARN', 'amqplib=WARN', 'boto=WARN',
                      'qpid=WARN', 'sqlalchemy=WARN', 'suds=INFO',
                      'oslo.messaging=INFO', 'iso8601=WARN',
                      'requests.packages.urllib3.connectionpool=WARN',
                      'urllib3.connectionpool=WARN', 'websocket=WARN',
                      "keystonemiddleware=WARN", "routes.middleware=WARN",
                      "stevedore=WARN"]

log_opts = [
    cfg.StrOpt('logging_context_format_string',
               default='%(asctime)s.%(msecs)03d %(process)d %(levelname)s '
                       '%(name)s [%(request_id)s %(user_identity)s] '
                       '%(instance)s%(message)s',
               help='Format string to use for log messages with context.'),
    cfg.StrOpt('logging_default_format_string',
               default='%(asctime)s.%(msecs)03d %(process)d %(levelname)s '
                       '%(name)s [-] %(instance)s%(message)s',
               help='Format string to use for log messages without context.'),
    cfg.StrOpt('logging_debug_format_suffix',
               default='%(funcName)s %(pathname)s:%(lineno)d',
               help='Data to append to log format when level is DEBUG.'),
    cfg.StrOpt('logging_exception_prefix',
               default='%(asctime)s.%(msecs)03d %(process)d TRACE %(name)s '
               '%(instance)s',
               help='Prefix each line of exception output with this format.'),
    cfg.ListOpt('default_log_levels',
                default=DEFAULT_LOG_LEVELS,
                help='List of logger=LEVEL pairs.'),
    cfg.BoolOpt('publish_errors',
                default=False,
                help='Enables or disables publication of error events.'),
    cfg.BoolOpt('fatal_deprecations',
                default=False,
                help='Enables or disables fatal status of deprecations.'),

    # NOTE(mikal): there are two options here because sometimes we are handed
    # a full instance (and could include more information), and other times we
    # are just handed a UUID for the instance.
    cfg.StrOpt('instance_format',
               default='[instance: %(uuid)s] ',
               help='The format for an instance that is passed with the log '
                    'message.'),
    cfg.StrOpt('instance_uuid_format',
               default='[instance: %(uuid)s] ',
               help='The format for an instance UUID that is passed with the '
                    'log message.'),
]

CONF = cfg.CONF
CONF.register_cli_opts(common_cli_opts)
CONF.register_cli_opts(logging_cli_opts)
CONF.register_opts(generic_log_opts)
CONF.register_opts(log_opts)
