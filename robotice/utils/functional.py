import sys

def import_module(name, _type="sensor", drivers_path="/srv/robotice/sensors"):
    """wrapper for import module
    
    drivers_path/name_module
    
    return name module
    """

    sys.path.append("/".join([drivers_path, name]))

    mod = __import__(_type)

    return mod