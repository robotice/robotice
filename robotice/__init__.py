import pbr.version

__version__ = pbr.version.VersionInfo('robotice').version_string()

ROBOTICE_BANNER="""
 ______       _                _             
(_____ \     | |           _  (_)            
 _____) )___ | |__   ___ _| |_ _  ____ _____ 
|  __  // _ \|  _ \ / _ (_   _) |/ ___) ___ |
| |  \ \ |_| | |_) ) |_| || |_| ( (___| ____|
|_|   |_\___/|____/ \___/  \__)_|\____)_____)    {0}
""".format(".".join([__version__, __release__]))

import os
import sys

# set some globals
os.environ.setdefault("R_WORKER_DIR", "/srv/robotice")
os.environ.setdefault("R_CONFIG_DIR", "/srv/robotice/config")
os.environ.setdefault("R_DRIVERS_DIR", "/srv/robotice/drivers")

# If ../robotice/__init__.py exists, add ../ to Python search path, so that
# it will override what happens to be installed in /usr/(local/)lib/python...
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir))

if os.path.exists(os.path.join(possible_topdir, 'robotice', '__init__.py')):
    sys.path.insert(0, possible_topdir)

