
"""
base object managers

"""

import sys
import logging

from robotice.conf.managers.base import BaseConfigManager


LOG = logging.getLogger(__name__)


class PlanManager(BaseConfigManager):

    config_path = "plans/*.yml"

plans = PlanManager()