
import os
import sys

def import_named_module(name, submodule=None):
    module = 'robotice.%s' % name
    if submodule:
        module = '.'.join((module, submodule))
    return __import__(module)

def import_module(module_dir, module_name="sensor", method="get_data", drivers_path=None):
    """wrapper for import module
    
    module_dir = dummy
    module_name = sensor ..
    
    return name module
    """
    DRIVERS_DIR = os.getenv("R_DRIVERS_DIR")
    #sys.path.append(DRIVERS_DIR)
    sys.path.append("%s/%s"%(DRIVERS_DIR, module_dir))

    try:
        mod = __import__("%s.%s" % (module_dir, module_name), globals(), locals(), method)
    except Exception, e:
        raise Exception("%s R_DRIVERS_DIR:%s" % (e, DRIVERS_DIR))

    return mod
