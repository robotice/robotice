import sys
import socket
import unittest
from statsd import Gauge

sys.path.append('/srv/robotice/service')

from robotice.conf import setup_app, RoboticeSettings, Settings

from nose.tools import assert_equals


class UtilTestCase(unittest.TestCase):

    def setUp(self):
        self.settings = setup_app('monitor')


    def test_setup_app(self):

        assert_equals(self.settings.hostname, socket.getfqdn())

        self.assertIsInstance(self.settings.config, dict)

        self.assertIsInstance(self.settings, Settings)

        # singleton test
        settings = RoboticeSettings("monitor")

        assert_equals(self.settings, settings)

        settings = setup_app('monitor')

        assert_equals(self.settings, settings)

        # change role

        assert_equals(self.settings.worker, "monitor")
        
        self.worker = setup_app('reasoner').worker
        
        assert_equals(self.worker, "reasoner")

        self.assertIsInstance(self.settings.config.get("metering"), dict)

        
    def test_broker(self):

        self.assertIsInstance(self.settings.broker, basestring)

    def test_metering(self):
        settings = RoboticeSettings("reasoner")

        assert_equals(settings.worker, "reasoner")
        
        self.assertIsInstance(settings.config.get("metering"), dict)

        self.assertIsInstance(self.settings.metering, Gauge)
