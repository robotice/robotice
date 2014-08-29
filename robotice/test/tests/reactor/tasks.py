import os
import sys
import unittest

sys.path.append('/srv/robotice/service')

from robotice.conf import setup_app, RoboticeSettings

from nose.tools import assert_equals, with_setup


def setUp(self):
    self.config = setup_app('monitor')

@with_setup(setUp)
def test_commit_action(self):
    pass