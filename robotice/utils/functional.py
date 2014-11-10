
import os
import sys

SENSORS_DIR = os.getenv("R_DRIVERS_DIR")

sys.path.append(SENSORS_DIR)

def import_module(module_dir, module_name="sensor", method="get_data", drivers_path=None):
    """wrapper for import module
    
    module_dir = dummy
    module_name = sensor ..
    
    return name module
    """

    mod = __import__("%s.%s" % (module_dir, module_name), globals(), locals(), method)

    return mod
