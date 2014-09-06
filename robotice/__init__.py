__title__ = 'Robotice'
__version__ = '0.0.1'
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
]