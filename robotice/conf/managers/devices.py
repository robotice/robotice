
"""
base object managers

"""

import sys
import logging

from robotice.conf.managers.base import BaseManager

LOG = logging.getLogger(__name__)

import glob
from yaml import load, dump, safe_dump


class DeviceManager(BaseManager):

	pass


devices = DeviceManager()