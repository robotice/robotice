# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import

import os

from oslo.config import cfg
import argparse
import sys

from oslo.config import types

import six
import sys

import logging
import argparse

# If ../../robotice/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'robotice', '__init__.py')):
    sys.path.insert(0, possible_topdir)

from robotice.conf import RoboticeSettings
from robotice.utils.output import output
from robotice import ROBOTICE_BANNER
from prettytable import PrettyTable
import json

from robotice.api import wsgi
from robotice.common.i18n import _

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

__version__ = "0.0.1"

cfg.CONF.config_file = "/srv/robotice/conf/api.conf"
cfg.CONF.debug = True

class BaseApp(object):

    name = None

    @classmethod
    def add_argument_parser(cls, subparsers):
        
        parser = subparsers.add_parser(cls.name, help=cls.__doc__)
        parser.set_defaults(cmd_class=cls)

        parser.add_argument('-d', '--debug', default=True, nargs='?',
                            help=('Debug.'))

        return parser

class Serve(BaseApp):

    """Start server
    api run 0.0.0.0 8004
    """

    name = 'run'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(Serve, cls).add_argument_parser(subparsers)
        parser.add_argument('bind_host', default='0.0.0.0', nargs='?',
                            help=('Bind host default 0.0.0.0.'))
        parser.add_argument('bind_port', default=8004,
                            help=('Bind port default 8004 '))

        return parser

    @staticmethod
    def main():
        try:
            LOG.debug('starting inicialization')

            app = wsgi.load_paste_app("robotice.api")

            port = CONF.command.bind_port
            host = CONF.command.bind_host
            LOG.info(_('Starting Robotice ReST API on %(host)s:%(port)s'),
                     {'host': host, 'port': port})
            server = wsgi.Server()
            server.start(app, CONF.command, default_port=port)
            server.wait()
        except RuntimeError as e:
            msg = six.text_type(e)
            sys.exit("ERROR: %s" % msg)

CMDS = [
    Serve,
]


def add_command_parsers(subparsers):
    for cmd in CMDS:
        cmd.add_argument_parser(subparsers)

command_opt = cfg.SubCommandOpt('command',
                                title='Commands',
                                help='Available commands',
                                handler=add_command_parsers)


def main(argv=None, config_files=None):
    CONF.register_cli_opt(command_opt)

    CONF(args=argv[2:],
         project='api',
         version=__version__,
         usage='%(prog)s [' + '|'.join([cmd.name for cmd in CMDS]) + ']',
         default_config_files=config_files)

    CONF.command.cmd_class.main()
