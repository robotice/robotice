import os
import sys
import logging
import unittest

LOG = logging.getLogger(__name__)

R_ROOT = getattr(os.environ, "R_ROOT_DIR", '/srv/robotice/service')

LOG.info(R_ROOT)
LOG.error(R_ROOT)

sys.path.append(R_ROOT)

from robotice.conf import setup_app, RoboticeSettings

from nose.tools import assert_equals


class MonitorTestCase(unittest.TestCase):

    def setUp(self):
        self.config = setup_app('monitor')

    def test_get_plan(self):
    	pass

    def test_get_real_data(self):
        pass

    def test_get_sensor_data(self):
        pass