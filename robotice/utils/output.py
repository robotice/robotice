import json
import yaml
    
def to_json(data, pretty_print=False):
    separators = (',', ': ') if pretty_print else (',', ':')
    indent = 2 if pretty_print else None
    return json.dumps(data, indent=indent, separators=separators)

def to_yaml(self, data, pretty_print=False):
    return yaml.dump(data, default_flow_style=not pretty_print)

def output(data, format="json", pretty_print=True):
	"""format output
	"""

	method = globals().get("to_%s" % format)

	result = None

	try:
		result = method(data, pretty_print)
	except Exception, e:
		raise e

	return result