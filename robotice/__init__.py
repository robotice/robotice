__title__ = 'Robotice'
__release__ = '54'
__version__ = '0.2'
__author__ = 'Ales Komarek & Michael Kuty'
__license__ = 'Apache 2.0'
__copyright__ = ''

try:
    from robotice.conf import RoboticeSettings
    from robotice.conf import Grains
except ImportError:
    pass
    #raise Exception("Could not import Robotice dependencies.")


__all__ = [
    "RoboticeSettings",
    "Grains",
    "ROBOTICE_BANNER",
]

ROBOTICE_BANNER="""
 ______       _                _             
(_____ \     | |           _  (_)            
 _____) )___ | |__   ___ _| |_ _  ____ _____ 
|  __  // _ \|  _ \ / _ (_   _) |/ ___) ___ |
| |  \ \ |_| | |_) ) |_| || |_| ( (___| ____|
|_|   |_\___/|____/ \___/  \__)_|\____)_____)    {0}
""".format(".".join([__version__, __release__]))