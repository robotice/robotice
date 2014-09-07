import os
import sys
import unittest

R_ROOT = getattr(os.environ, "R_ROOT_DIR", '/srv/robotice/service')

sys.path.append(R_ROOT)

from robotice.conf import setup_app, RoboticeSettings

from nose.tools import assert_equals, with_setup

class ReactorTestCase(unittest.TestCase):

    def setUp(self):
        self.config = setup_app('reactor')

    def test_commit_action(self):
        pass