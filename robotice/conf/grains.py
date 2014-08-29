
class Grains(object):
    """grains generated from salt
    """

    hostname = None
    os_family = None
    cpu_arch = None
    
    def __init__(self):

        grains_file = open("/srv/robotice/grains.yml", "r")
        grains = load(grains_file)['grains']

        self.hostname = grains['hostname']
        self.os_family = grains['os_family']
        self.cpu_arch = grains['cpu_arch']

grains = Grains()