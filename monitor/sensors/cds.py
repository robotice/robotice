#!/usr/bin/python
import subprocess

executable = "/srv/robotice/sensors/cds/cds_driver.py"

def get_cds_data(sensor):

	value = subprocess.check_output([executable, str(port), str(arch)]);

	data = []
    data.append( ["cds.%s.luminosity" % sensor.get('device'), int(value)] )

    return data
