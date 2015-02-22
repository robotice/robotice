__title__ = 'Robotice'
__release__ = '1'
__version__ = '0.2.6'
__author__ = 'Ales Komarek & Michael Kuty'
__license__ = """
Copyright 2014 Ales Komarek & Michael Kuty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
__copyright__ = ''

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

