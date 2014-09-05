import subprocess

executable = "/srv/robotice/sensors/hygro/driver.py"

def clean_value(value):
	vals = value.split(",")
	
	r = None

	for v in vals:
		try:
			r = int(v)
		except Exception, e:
			pass
		if r:
			return r
	return r

def get_data(sensor):

    port = str(sensor.get('port'))

    arch = sensor.get('cpu_arch')

    value = subprocess.check_output(
        [executable, '-%s' % sensor.get("type").upper(), str(port), '-a', str(arch)])

    data = []

    metric_format = "{0}.hygro_{1}"

    data.append((metric_format.format(sensor.get('name'), sensor.get("type").lower()), clean_value(value),))

    return data