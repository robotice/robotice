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
import json
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
import pyaml

from robotice.reactor.app import app
from robotice.utils import tasks

from celery.events import Events

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

__version__ = "0.0.1"


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

        return parser

class PlanList(BaseApp):

    name = 'list'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(PlanList, cls).add_argument_parser(subparsers)
        parser.add_argument('-w', '--worker', default=None,
                            help=('Ping only Scpecific Worker.'))
        return parser


    @staticmethod
    def stdout(tasks):
        x = PrettyTable(["ID", "Task"])

        for task in tasks:
            x.add_row([task[0], task[1]])

        print x

    @staticmethod
    def main():

        config = setup_app("reasoner")
        data = config.plan_manager.list()
        data.p() # print

class PlanGet(BaseApp):

    name = 'get'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(PlanGet, cls).add_argument_parser(subparsers)
        parser.add_argument('uuid', default=None,
                            help=('UUID of plan'))
        return parser


    @staticmethod
    def stdout(tasks):
        x = PrettyTable(["ID", "Task"])

        for task in tasks:
            x.add_row([task[0], task[1]])

        print x

    @staticmethod
    def main():

        config = setup_app("reasoner")
        data = config.plan_manager.get(CONF.command.uuid)
        print data

class PlanUpdate(BaseApp):

    name = 'set'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(PlanUpdate, cls).add_argument_parser(subparsers)
        parser.add_argument('key', default=None,
                            help=('Key'))
        parser.add_argument('value', default=None,
                            help=('Value'))
        return parser

    @staticmethod
    def main():

        config = setup_app("reasoner")
        value = CONF.command.value
        try:
            value = json.loads(CONF.command.value)
        except Exception, e:
            pass
        data = config.plan_manager.set(CONF.command.key, value)
        print data

CMDS = [
    PlanList,
    PlanGet,
    PlanUpdate,
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
         project='reactor',
         version=__version__,
         usage='%(prog)s [' + '|'.join([cmd.name for cmd in CMDS]) + ']',
         default_config_files=config_files)

    CONF.command.cmd_class.main()
