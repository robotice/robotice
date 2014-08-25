import sys
import socket
import unittest

sys.path.append('/srv/robotice/service')

from utils import setup_app


class UtilTestCase(unittest.TestCase):

    def setUp(self):
        self.settings = setup_app('monitor')

    def test_setup_app(self):
        self.assertEqual(self.settings.hostname, socket.getfqdn())
        self.assertIsInstance(self.settings.config, dict)
