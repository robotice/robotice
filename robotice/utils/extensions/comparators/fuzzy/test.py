
import fuzzy.storage.fcl.Reader

system = fuzzy.storage.fcl.Reader.Reader().load_from_file("/srv/robotice/config/fuzzy/fan1.fcl")

sensor_output = {
    "real_value": 70.0
}
output = {
    "action": 0.0
}

for x in range(0, 100):
	sensor_output["real_value"] = x
	print "input: %s output: %s" % (x,system.calculate(sensor_output, output)["action"])