#!/usr/bin/python
import subprocess

executable = "/srv/robotice/sensors/cds/cds_driver.py"

def get_cds_data(sensor):

    value = subprocess.check_output([executable, str(sensor.get('port')), sensor.get('cpu_arch')])

    data = []
    data.append(["cds.%s.luminosity" % sensor.get('device'), int(value)])

    return data
