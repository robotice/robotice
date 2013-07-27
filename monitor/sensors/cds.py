#!/usr/bin/python
import subprocess

executable = "/srv/robotice/sensors/cds/cds.py"

def get_cds_data(sensor):

    data = []
    data.append( ["cds.%s.luminosity" % sensor.get('device'), 40] )

    return data
