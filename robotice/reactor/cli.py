#!/usr/bin/env python
"""

Simple reactor CLI.

"""

import argparse
import sys

from oslo.config import cfg
from oslo.config import types

sys.path.append("../")

from robotice.conf import RoboticeSettings
from robotice.utils.output import output
from robotice import ROBOTICE_BANNER
from prettytable import PrettyTable
import json


__version__ = "0.0.1"

common_opts = [
    cfg.StrOpt('task',
               short='t',
               help="Task name",
               required=True),
    cfg.StrOpt('args',
               short='a',
               default='',
               help='Args - json format {}',
               required=False),
    cfg.StrOpt('kwargs',
               short='k',
               default='',
               help='Kwargs',
               required=False),
    cfg.StrOpt('queue',
               short='q',
               default="",
               help='Queue',
               required=True),
    cfg.StrOpt('exchange',
               short='e',
               default="",
               help='Exchange',
               required=False),
    #cfg.SubCommandOpt('action', handler=add_parsers),
]
CONF = cfg.CONF
CONF.register_cli_opts(common_opts)

CONF.__call__(
    project="Robotice",
    prog=ROBOTICE_BANNER,
    version=__version__)

CONF(sys.argv[1:])

"""
python robotice-reactor.py -t 'reactor.commit_action' --a='{"os_family":"Arch","socket":3,"device":"sispm","port":0}' -q reactor


python robotice-reactor.py -t 'reactor.commit_action' -k '{"os_family":"Arch","socket":3,"device":"sispm","port":0}' -q reactor

"""

from robotice.worker_reactor import celery as reactor

# Positional args.
args = CONF.get('args') or ()
if isinstance(args, str):
    args = json.loads(args)

# Keyword args.
kwargs = CONF.get('kwargs') or {}
if isinstance(kwargs, str):
    kwargs = json.loads(kwargs)

result = reactor.send_task(
    CONF.task, args=list(args), kwargs=kwargs, queue=CONF.queue, exhcange=CONF.exchange)

print result