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

from robotice.conf import RoboticeSettings, setup_app
from robotice.utils.output import output
from robotice import ROBOTICE_BANNER
from prettytable import PrettyTable
import json
import pyaml
from robotice.reactor.app import app
from robotice.utils import tasks

from celery.events import Events

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

__version__ = "0.0.1"


def pp(data):

    return pyaml.pprint(data.convert_to(data))

class BaseApp(object):

    name = None

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help=cls.__doc__)
        parser.set_defaults(cmd_class=cls)

        parser.add_argument('-d', default=True, nargs='?',
                            help=('Debug.'))
        parser.add_argument('-a', '--args', default=(), nargs='?',
                            help=('Arguments for send task.'))
        parser.add_argument('-k', '--kwargs', default={},
                            help=('Kwargs for send task.'))

        parser.add_argument('config', default=None,
                            help=('plans, devices, systems, actions ...'))
        return parser

class ItemList(BaseApp):

    name = 'list'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(ItemList, cls).add_argument_parser(subparsers)
        return parser

    @staticmethod
    def main():

        config = setup_app("reasoner")

        manager = getattr(config, CONF.command.config)
        pp(manager.list())


class ItemGet(BaseApp):

    name = 'get'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(ItemGet, cls).add_argument_parser(subparsers)
        parser.add_argument('key', default=None,
                            help=('Key with : notation like a my_box.actuators'))
        return parser

    @staticmethod
    def main():

        config = setup_app("reasoner")
        manager = getattr(config, CONF.command.config)
        data = manager.get(CONF.command.key)
        try:
            pp(data)
        except Exception, e:
            print data

class ItemUpdate(BaseApp):

    name = 'set'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(ItemUpdate, cls).add_argument_parser(subparsers)
        parser.add_argument('key', default=None,
                            help=('Key'))
        parser.add_argument('value', default=None,
                            help=('Value'))
        return parser

    @staticmethod
    def main():

        config = setup_app("reasoner")
        manager = getattr(config, CONF.command.config)
        value = CONF.command.value
        try:
            value = json.loads(CONF.command.value)
        except Exception, e:
            pass
        data = manager.set(CONF.command.key, value)
        print data

CMDS = [
    ItemList,
    ItemGet,
    ItemUpdate,
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
         project='robotice',
         version=__version__,
         usage='%(prog)s [' + '|'.join([cmd.name for cmd in CMDS]) + ']',
         default_config_files=config_files)

    CONF.command.cmd_class.main()
