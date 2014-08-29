
def import_module(name):
	"""wrapper for inport module
	name:string  monitor.sensors.afm
	return afm module
	"""
    mod = __import__(name)
    components = name.split('.')

    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod