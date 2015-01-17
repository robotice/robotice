
"""
base object managers

"""

import sys
import logging

from robotice.conf.managers.base import BaseConfigManager


LOG = logging.getLogger(__name__)


class DeviceManager(BaseConfigManager):

    config_path = "devices/*.yml"

devices = DeviceManager()