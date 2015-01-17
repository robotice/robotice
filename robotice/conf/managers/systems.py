
"""
base object managers

"""

import sys
import logging

from robotice.conf.managers.base import BaseConfigManager


LOG = logging.getLogger(__name__)


class SystemManager(BaseConfigManager):

    config_path = "systems/*.yml"

systems = SystemManager()