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
import socket

# If ../../robotice/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'robotice', '__init__.py')):
    sys.path.insert(0, possible_topdir)

from robotice.utils.output import output
from robotice.common.importutils import import_module
from robotice import ROBOTICE_BANNER

from celery import concurrency
from celery.platforms import maybe_drop_privileges
from celery.utils.log import LOG_LEVELS, mlevel

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

__version__ = "0.0.1"


class BaseApp(object):

    name = None

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help=cls.__doc__)
        parser.set_defaults(cmd_class=cls)
        parser.add_argument('-d', '--debug', default=True, nargs='?',
                            help=('Debug.'))
        parser.add_argument('-l', '--loglevel', default="WARNING", help=('LOG Level.'))
        parser.add_argument('-B', '--beat', default=False, action='store_true',
                            help=('start with Beat.'))
        parser.add_argument('-E', '--events', default=True, action='store_true',
                            help=('Events.'))
        return parser

class RunDaemon(BaseApp):

    """Sync the database.
    Example use:
    
    ..code-block: bash
        
        robotice run reactor
    """

    name = 'run'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(RunDaemon, cls).add_argument_parser(subparsers)

        parser.add_argument('worker', default=None, nargs='?',
                            help=('Worker name. [monitor, reactor, reasoner, planner]'))

        return parser

    @staticmethod
    def run(argv=None, hostname=None, pool_cls=None, app=None, uid=None, gid=None,
            loglevel=None, logfile=None, pidfile=None, state_db=None,
            **kwargs):

        _worker_role = getattr(CONF, "worker", argv[2])
        try:
            w = import_module("robotice.%s.app" % _worker_role)
        except Exception, e:
            LOG.error(e)
            raise e

        app = w.app

        maybe_drop_privileges(uid=uid, gid=gid)
        # Pools like eventlet/gevent needs to patch libs as early
        # as possible.
        pool_cls = (concurrency.get_implementation(pool_cls) or
                    app.conf.CELERYD_POOL)

        if _worker_role == "reasoner":
            kwargs["beat"] = True

        hostname = hostname or _worker_role + "@" + socket.getfqdn()
        if loglevel:
            try:
                loglevel = mlevel(loglevel)
            except KeyError:  # pragma: no cover
                LOG('Unknown level {0!r}. Please use one of {1}.'.format(
                    loglevel, '|'.join(
                        l for l in LOG_LEVELS if isinstance(l, string_t))))

        worker = app.Worker(
            hostname=hostname, pool_cls=pool_cls, loglevel=loglevel,
            logfile=logfile,  # node format handled by celery.app.log.setup
            **kwargs
        )
        worker.start()
        return worker.exitcode

    def main(self, argv):
        RunDaemon.run(argv, loglevel=CONF.command.loglevel)
        LOG.error(worker)

CMDS = [
    RunDaemon,
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

    CONF(args=argv[1:],
         project='robotice',
         version=__version__,
         usage='%(prog)s [' + '|'.join([cmd.name for cmd in CMDS]) + ']',
         default_config_files=config_files)
    CONF.command.cmd_class().main(argv)
"""

def main(argv=None):
    try:
        args = argv[2:]

        RunDaemon().main(args)
    except KeyboardInterrupt:
        print "... bye"
        sys.exit(130)
    except Exception as e:
        if '--debug' in args or '-d' in args:
            raise e
        
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
