import os
import sys
import unittest
from conf import setup_app, RoboticeSettings

from nose.tools import assert_equals

sys.path.append('/srv/robotice/service')

class MonitorTestCase(unittest.TestCase):

    def setUp(self):
        self.config = setup_app('monitor')

    def test_get_plan(self):
    	pass

    def test_get_real_data(self):
        pass

    def test_get_sensor_data(self):
        pass