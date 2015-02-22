#!/usr/bin/env python

from __future__ import absolute_import

import os
import six
import sys

import argparse

# If ../robotice/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'robotice', '__init__.py')):
    sys.path.insert(0, possible_topdir)

import robotice
from robotice.conf import config

from robotice.utils import cliutils as utils

from robotice.common.i18n import _
from robotice.common.importutils import import_module

import logging

LOG = logging.getLogger(__name__)


class RoboticeShell(object):

    def _setup_logging(self, debug):
        log_lvl = logging.DEBUG if debug else logging.WARNING
        logging.basicConfig(
            format="%(levelname)s (%(module)s) %(message)s",
            level=log_lvl)
        logging.getLogger('iso8601').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    def _setup_verbose(self, verbose):
        if verbose:
            exc.verbose = 1

    def get_subcommand_parser(self, name):
        parser = self.get_base_parser()

        self.subcommands = {}
        subparsers = parser.add_subparsers(metavar='<subcommand>')
        submodule = import_module(name, 'shell')

        self._find_actions(subparsers, submodule)
        self._find_actions(subparsers, self)
        self._add_bash_completion_subparser(subparsers)

        return parser

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            prog='robotice',
            description=robotice.ROBOTICE_BANNER,
            epilog=_('See "%(arg)s" for help on a specific command.') % {
                'arg': 'robotice help COMMAND'
            },
            add_help=False,
            formatter_class=HelpFormatter,
        )

        # Global arguments

        parser.add_argument('-r', '--role',
                            help=_("action [reactor, monitor, planner, reasoner, conf]"))

        parser.add_argument('-h', '--help',
                            action='store_true',
                            help=argparse.SUPPRESS)

        parser.add_argument('--version',
                            action='version',
                            version=robotice.__version__,
                            help=("Shows the Robotice version."))

        parser.add_argument('-d', '--debug',
                            default=bool(utils.env('ROBOTICE_DEBUG')),
                            action='store_true',
                            help=('Defaults to %(value)s.') % {
                                'value': 'env[ROBOTICE_DEBUG]'
                            })

        parser.add_argument('-v', '--verbose',
                            default=False, action="store_true",
                            help=("Print more verbose output."))

        return parser

    def main(self, argv):
        # Parse args once to find role
        parser = self.get_base_parser()
        (options, args) = parser.parse_known_args(argv)
        self._setup_logging(options.debug)
        self._setup_verbose(options.verbose)

        # build available subcommands based on version
        r_role = options.role or argv[0]

        try:
            if r_role in ["monitor", "reactor", "reasoner", "planner", "api", "conf"]:
                mod = import_module("robotice.%s.shell" % r_role)
            elif r_role == "run":
                mod = import_module("robotice.shell")
            mod.main(argv=sys.argv)
        except Exception, e:
            if '--debug' in argv or '-d' in argv:
                raise e
            parser.print_help()

class HelpFormatter(argparse.RawDescriptionHelpFormatter):

    def start_section(self, heading):
        # Title-case the headings
        heading = '%s%s' % (heading[0].upper(), heading[1:])
        super(HelpFormatter, self).start_section(heading)


def main(args=None):
    try:
        if args is None:
            args = sys.argv[1:]

        RoboticeShell().main(args)
    except KeyboardInterrupt:
        print "... bye"
        sys.exit(130)
    except Exception as e:
        if '--debug' in args or '-d' in args:
            raise e
        # ugly hack
        RoboticeShell().get_base_parser().print_help()
        
        sys.exit(1)

if __name__ == "__main__":
    main()
