import sys
import socket
import unittest

sys.path.append('/srv/robotice/service')

from robotice.conf import setup_app, RoboticeSettings

from nose.tools import assert_equals

class UtilTestCase(unittest.TestCase):

    def setUp(self):
        self.settings = setup_app('monitor')

    def test_setup_app(self):
        assert_equals(self.settings.hostname, socket.getfqdn())
        assert_equals(self.settings.config, dict)
        
        assert_equals(self.settings, RoboticeSettings)

        assert_equals(self.settings, RoboticeSettings)
