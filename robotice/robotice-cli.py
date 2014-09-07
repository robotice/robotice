#!/usr/bin/env python
"""

Simple CLI for easy debuging.

"""

import argparse

from robotice.conf import RoboticeSettings
from robotice.utils.output import output

def inspect_config(role, pretty_print=True):
    """print all loaded configuration
    """

    conf = RoboticeSettings(role)

    print output(conf.config)

    if role == "reasoner":

        print output(conf.sensors)

        print output(conf.actuators)

        print output(conf.plans)


def nodeinfo(node):
    """return nodeinfo independent on location in cluster

    note: can be call only on reaoner.
    """
    
    conf = RoboticeSettings("reasoner")
    plan_name = None
    
    for system in conf.systems:
        if node in system.get("name"):
            print system
            plan_name = system.get("plan")

    for device in conf.devices:
        if node in device.get("host"):
            print device

    plan_printed = False
    
    for plan in conf.plans:
        if plan.get("name") == plan_name:
            print plan
            plan_printed = True

    if not plan_printed:
        print "Plan %s not found" % plan


def status():
    """return status for all services

    """

    print """
        Monitor      ........   :-)
        Planner      ........   :-)
        Reasoner     ........   :-)
        Reactor      ........   :-)
    """

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="""
     ______       _                _             
    (_____ \     | |           _  (_)            
     _____) )___ | |__   ___ _| |_ _  ____ _____ 
    |  __  // _ \|  _ \ / _ (_   _) |/ ___) ___ |
    | |  \ \ |_| | |_) ) |_| || |_| ( (___| ____|
    |_|   |_\___/|____/ \___/  \__)_|\____)_____)   0.0.1
    """)
parser.add_argument("-c", "--conf",
                    help="default: /srv/robotice/conf", default="/srv/robotice/conf")
parser.add_argument("-w", "--workerconf", dest="worker configuration PATH",
                    help="worker configuration PATH", default="/srv/robotice")
parser.add_argument("-l", "--nodeinfo",
                    dest="nodeinfo",
                    help="don't print status messages to stdout")
parser.add_argument("-i", "--inspect",
                    help="print configuration expect role `reasoner` for example.")
parser.add_argument("-s", "--status",
                    default=False,
                    help="print status for all services",
                    action="store_true")


opts = parser.parse_args()

INPUT = False

if __name__ == "__main__":

    if opts.inspect:
        inspect_config(opts.inspect)
        INPUT = True

    if opts.status:
        status()
        INPUT = True

    if opts.nodeinfo:
        nodeinfo(opts.nodeinfo)
        INPUT = True

    if not INPUT:
        parser.print_help()
