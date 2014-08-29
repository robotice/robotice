import os
import sys
import unittest

sys.path.append('/srv/robotice/service')

from robotice.conf import setup_app, RoboticeSettings

from nose.tools import assert_equals, with_setup

class ReactorTestCase(unittest.TestCase):

    def setUp(self):
        self.config = setup_app('reactor')

    def test_commit_action(self):
        pass