import subprocess

executable = "/srv/robotice/sensors/cds/driver.py"

def get_data(sensor):
    port = str(sensor.get('port'))
    arch = sensor.get('cpu_arch')

    value = subprocess.check_output([executable, '-p', str(port), '-a', str(arch)])

    data = []

    data.append(("%s.luminosity" % sensor.get('name'), int(value),))

    return data
