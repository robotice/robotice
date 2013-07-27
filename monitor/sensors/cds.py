import subprocess

executable = "/srv/robotice/sensors/cds/driver.py"

def get_cds_data(sensor):

    value = subprocess.check_output([executable, '-p', str(sensor.get('port')), '-a', sensor.get('cpu_arch')])

    data = []
    data.append(["cds.%s.luminosity" % sensor.get('device'), int(value)])

    return data
