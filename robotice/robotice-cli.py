#!/usr/bin/env python
"""

Simple CLI for easy debuging.

"""

import argparse
import sys

sys.path.append("../")

from robotice.conf import RoboticeSettings
from robotice.utils.output import output

from robotice import ROBOTICE_BANER

from prettytable import PrettyTable  

def inspect_config(role, pretty_print=True):
    """print all loaded configuration
    """

    conf = RoboticeSettings(role)

    print output(conf.config)




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
    x = PrettyTable()
    x.add_column("Role",["Monitor","Reasoner","Planner","Reactor","Control"])
    x.add_column("Status",["OK","OK","OK","OK","OK"])

    #x.get_string(fields=["Role", "Status"])

    print x.get_string() 

    try:
        conf = RoboticeSettings("reasoner")
        x = PrettyTable()
        x.add_column("Stat",["Sensors","Actuators","Systems","Plans"])
        x.add_column("Count",[len(conf.sensors), len(conf.actuators),
            len(conf.systems), len(conf.plans)])
        
        print x.get_string()
    except Exception, e:
        pass


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=ROBOTICE_BANER)
parser.add_argument("-c", "--conf",
                    help="default: /srv/robotice/conf", default="/srv/robotice/conf")
parser.add_argument("-w", "--workerconf",
                    help="default: /srv/robotice", default="/srv/robotice")
parser.add_argument("-l", "--nodeinfo",
                    dest="nodeinfo",
                    help="-l ubuntu1")
parser.add_argument("-i", "--inspect",
                    help="print worker configuration -i reasoner")
parser.add_argument("-s", "--status",
                    default=False,
                    help="print robotice status",
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
