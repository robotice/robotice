import subprocess

executable = "/srv/robotice/sensors/cds/driver.py"

def get_data(sensor):
    port = str(sensor.get('port'))
    arch = sensor.get('cpu_arch')
    mode = sensor.get('mode')
    value = subprocess.check_output([executable, '-p', port, '-a', arch, '-m', mode])

    data = []

    data.append(("cds.%s.luminosity" % sensor.get('device'), int(value),))

    return data
