import os

import logging
from yaml import load

LOG = logging.getLogger(__name__)

class Grains(object):
    """grains generated from salt
    note: not using now 
    
    excepted structure:
    
    .. code-block:: yaml

        grains:
          hostname: redis1.box.robotice.cz
          os_family: Debian
          cpu_arch: amd64
    
    """
    
    def __init__(self, path="/srv/robotice"):

        try:
            R_GRAINS_DIR = getattr(os.environ, "R_GRAINS_DIR", path)
            _path = "".join([R_GRAINS_DIR,"/grains.yml"])
            grains_file = open(_path, "r")
            grains = load(grains_file)['grains']
        except IOError, e:
            LOG.error("Missing grains file %s: %s" % (path, e))

        self.hostname = grains['hostname']
        self.os_family = grains['os_family']
        self.cpu_arch = grains['cpu_arch']

grains = Grains()